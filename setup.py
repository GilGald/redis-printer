import os
import threading
import time
from time import sleep

import redis

from services.job_poller import JobPoller
from services.printer_queue_watcher import PrinterQueueWorker

is_connected = False
timeout = time.time() + 50
while not is_connected and timeout > time.time():
    try:
        conn = redis.StrictRedis(host="redis1")

        conn.ping()
        is_connected = True
    except redis.exceptions.ConnectionError as e:
        print("waiting for redis connection")
        sleep(0.7)

if not is_connected:
    print("could not connect")
else:
    t = threading.Thread(name='job_poll',
                         target=JobPoller().poll_jobs,
                         args=[conn])
    t.start()

    for i in range(1, 2):
        name = 'print_queue' + str(i)
        threading.Thread(name=name,
                         target=PrinterQueueWorker().do_job,
                         args=[conn, name]).start()
