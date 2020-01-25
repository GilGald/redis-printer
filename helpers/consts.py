class Consts:
    QUEUE = "queue:"
    DELAYED_JOBS = "delayed:jobs"
    PRINTER_QUEUE = QUEUE + "printer_queue"

    @classmethod
    def wrap_with_queue(cls, queue_name):
        return cls.QUEUE+queue_name
