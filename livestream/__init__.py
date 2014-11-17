# -*- coding: utf-8 -*-

from gevent import monkey
# see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/65
monkey.patch_all()

from flask import Flask
from flask.ext.socketio import SocketIO
import config
from Queue import Queue

# from werkzeug.contrib.cache import MemcachedCache
# cache = MemcachedCache(['127.0.0.1:11211'])

app = Flask(__name__)
app.config.from_object(config)
app.queue = Queue()

socketio = SocketIO(app)

from views import *
