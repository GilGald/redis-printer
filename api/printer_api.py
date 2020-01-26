import redis
from flask import Flask, request

from helpers.consts import Consts
from services.job_creator import JobCreator

app = Flask(__name__)
app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/echo', methods=['POST'])
def echo_at_time():
    """
    get time and message and creates a scheduled task to print the message
    e.g: calling echoAtTime with params:(10,hello)
    will print the message hello in 10 seconds

    :param time: time in seconds from now to print message
    :param msg: the message to print
    :return:
    """
    time = request.form['time']
    msg = request.form['msg']

    request_id = JobCreator().execute_later(conn=redis.StrictRedis(host="redis1"),
                                            queue_name=Consts.PRINTER_QUEUE,
                                            data={"msg": msg},
                                            delay=int(time))

    return f"Will print {msg} in {time} seconds\n-requestId :{request_id}\t\n"


@app.route('/')
def get():
    return "hello from printer server"
