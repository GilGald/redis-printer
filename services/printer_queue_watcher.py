import json

from helpers.consts import Consts


class PrinterQueueWorker(object):
    def do_job(self, conn,worker_name):
        print(f"* PrinterQueueWorker {worker_name}*")

        while True:
            item = conn.blpop(Consts.PRINTER_QUEUE, 10)

            if not item:
                continue

            _, _, data = json.loads(item[1])
            print(f"from worker {worker_name} message: {data['msg']} ")
