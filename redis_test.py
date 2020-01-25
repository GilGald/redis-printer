import time

import redis
from redis import Redis

# r = Redis()
r = redis.StrictRedis()
#
# r.set("name", "test")
# print(r.get("name"))
#
# r.set("name", "gil3")
# print(r.get("name"))

# data = [("now", 1), ("later", 1), ("even later", 1)]
# for d, s in data:
#     r.zadd("delayed:", {d: time.time()+s})
#
# zrange = r.zrange('delayed:', 0, 0, withscores=True)
# print(zrange)


r.rpush("queue:print_job")