from flask import Flask
from rq import Queue
from worker import conn

q = Queue(connection=conn)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app
