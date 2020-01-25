import json
import time
import uuid

from services.printer_queue_watcher import Consts


class JobCreator(object):

    def execute_later(self, conn, queue_name, data, delay=0):
        identifier = str(uuid.uuid4())
        # Generate a unique identifier.

        item = json.dumps([identifier, queue_name, data])

        # Prepare the item for the queue.
        if delay > 0:
            conn.zadd(Consts.DELAYED_JOBS, {item: time.time() + delay})
        # Delay the item.

        else:
            conn.rpush(Consts.wrap_with_queue(queue_name), item)
            # Execute the item immediately.

        return identifier


