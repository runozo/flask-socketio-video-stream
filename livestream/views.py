# -*- coding: utf-8 -*-
from __future__ import print_function
from livestream import app, socketio, cache
from flask import render_template, g, Response
from flask.ext.socketio import emit


def gen_livestream():
    """Video streaming generator function."""

    def _dog():
        fh = open("livestream/static/funny-dogs.jpg", "rb")
        frame = fh.read()
        fh.close()
        return frame

    while True:
        queue = cache.get('queue')
        if queue:
            # fh = open(str(len(queue)) + ".jpg", "wb")
            frame = queue.pop().split('base64')[-1].decode('base64')

            if not frame:
                frame = _dog()
            else:
                cache.set('queue', queue)
        else:
            frame = _dog()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               # b'Content-Type: image/webp\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def home():
    """The home page with webcam"""
    return render_template('video_test.html')


@app.route("/view")
def view():
    """The client page"""
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
    queue = cache.get('queue')
    if queue:
        queue.insert(0, message['data'])
    else:
        queue = [message['data']]
    # emit('response', '')
    # print(len(message['data']))
    cache.set('queue', queue)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_livestream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
