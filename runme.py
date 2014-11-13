# -*- coding: utf-8 -*-
from __future__ import print_function
from livestream import app, socketio, cache
from flask import render_template, g, Response
from flask.ext.socketio import emit


def gen_livestream():
    """Video streaming generator function."""
    while True:
        queue = cache.get('queue')
        if queue:
            frame = queue.pop()
            cache.set('queue', queue, timeout=5 * 60)
            print(frame)
        else:
            frame = ''
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def home():
    return render_template('video_test.html')


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
    """Video streaming reader. It's supposed that the stream will come from some javascript client side."""
    #queue = cache.get('queue')
    # if queue:
    #    queue.insert(0, message['data'])
    # else:
    #    queue = [message['data']]
    emit('response', '')
    print(message['data'])

    #cache.set('queue', queue, timeout=5 * 60)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of a video tag."""
    return Response(gen_livestream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    socketio.run(app)
