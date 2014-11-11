# -*- coding: utf-8 -*-
from gevent import monkey
# see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/65
monkey.patch_all()

from flask import Flask
from flask.ext.socketio import SocketIO
import config

app = Flask(__name__)

app.config.from_object(config)
socketio = SocketIO(app)
