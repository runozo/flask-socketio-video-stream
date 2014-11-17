# -*- coding: utf-8 -*-

from __future__ import print_function
from livestream import app, socketio
from flask import render_template, Response
from flask.ext.socketio import emit


def gen_livestream():
    """Video streaming generator function."""

    def _dog():
        """Returns a dog frame."""
        fh = open("livestream/static/funny-dogs.jpg", "rb")
        frame = fh.read()
        fh.close()
        return frame

    while True:
        if app.queue.qsize():
            frame = app.queue.get().split('base64')[-1].decode('base64')
        else:
            frame = _dog()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               # b'Content-Type: image/webp\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def home():
    """The home page with webcam."""
    return render_template('video_test.html')


@app.route("/view")
def view():
    """The client page."""
    return render_template('client.html')


@socketio.on('connect', namespace='/live')
def test_connect():
    """Connect event."""
    print('Client wants to connect.')
    emit('response', {'data': 'OK'})


@socketio.on('disconnect', namespace='/live')
def test_disconnect():
    """Disconnect event."""
    print('Client disconnected')


@socketio.on('event', namespace='/live')
def test_message(message):
    """Simple websocket echo."""
    emit('response',
         {'data': message['data']})
    print(message['data'])


@socketio.on('livevideo', namespace='/live')
def test_live(message):
    """Video stream reader."""
    app.queue.put(message['data'])


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_livestream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
