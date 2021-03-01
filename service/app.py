"""
Микросервис для обнаружения хостов в сети
Dmitry Livanov, 2021
ver 0.0.1
"""
from flask import request, abort
from runner import app
from service import q
from service.task import get_hosts


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



