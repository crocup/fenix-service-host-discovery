"""
Микросервис для обнаружения хостов в сети
Dmitry Livanov, 2021
ver 0.0.1
"""
from flask import Flask, request, abort
from rq import Queue
from task import get_hosts
from worker import conn

app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/api/v1/host_discovery/get', methods=['POST'])
def get_task():
    """

    :return:
    """
    if request.method == "POST":
        if not request.json or not 'host' in request.json:
            abort(400)
        data = request.json
        job = q.enqueue_call(
            func=get_hosts, args=(data['host'],), result_ttl=500
        )
    else:
        abort(400)
    return job.get_id()


if __name__ == '__main__':
    app.run(port=9001)
