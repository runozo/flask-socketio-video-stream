# -*- coding: utf-8 -*-
from __future__ import print_function
from livestream import app, socketio


if __name__ == "__main__":
    socketio.run(app)
