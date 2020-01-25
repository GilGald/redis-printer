import threading

import redis

from services.job_poller import JobPoller
from services.printer_queue_watcher import PrinterQueueWorker

conn = redis.StrictRedis()


t = threading.Thread(name='job_poll',
                     target=JobPoller().poll_jobs,
                     args=[conn])

for i in range(1, 2):
    name = 'print_queue' + str(i)
    threading.Thread(name=name,
                     target=PrinterQueueWorker().do_job,
                     args=[conn, name]).start()

t.start()
