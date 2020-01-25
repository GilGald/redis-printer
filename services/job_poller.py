import json
import time
import uuid

import redis

from helpers.consts import Consts


class JobPoller(object):
    # while true jobs and execute them

    def acquire_lock(self, conn, lockname, acquire_timeout=10):
        identifier = str(uuid.uuid4())

        end = time.time() + acquire_timeout
        while time.time() < end:
            if conn.setnx('lock:' + lockname, identifier):
                print(f"lock name {lockname}")
                return identifier

            time.sleep(.001)

        return False

    def release_lock(self, conn, lockname, identifier):
        pipe = conn.pipeline(True)
        lockname = 'lock:' + lockname

        while True:
            try:
                pipe.watch(lockname)
                if pipe.get(lockname) == identifier:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True

                pipe.unwatch()
                break

            except redis.exceptions.WatchError:
                pass
            return False

    def poll_jobs(self, conn):
        print("*Start listening for new jobs*")
        while 1:
            # Get the first item in the queue.
            item = conn.zrange(Consts.DELAYED_JOBS, 0, 0, withscores=True)

            # in case nothing to execute now
            if not item or item[0][1] > time.time():
                time.sleep(1)
                continue

            item = item[0][0]
            identifier, queue, _ = json.loads(item)

            # Unpack the item so that we know where it should go.

            locked = self.acquire_lock(conn, identifier)
            if not locked:
                # Get the lock for the item.

                # We couldn’t get the lock, so skip it and try again.
                continue

            remove_result = conn.zrem(Consts.DELAYED_JOBS, item)
            if remove_result:
                conn.rpush(queue, item)

            # Move the item to the proper list queue.

            self.release_lock(conn, identifier, locked)
