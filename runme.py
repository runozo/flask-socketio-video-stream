from __future__ import print_function
from livestream import app, socketio
from flask import render_template, g, Response
from flask.ext.socketio import emit


def gen_livestream():
    """Video streaming generator function."""
    return
    if not g.livestream:
        g.livestream = []
    while True:
        frame = g.livestream.pop()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def hello():
    return render_template('video_test.html')


@socketio.on('connect', namespace='/live')
def test_connect(namespace='/live'):
    print('Connecting')
    emit('response', {'data': 'I\'m Server: I\'m connected', 'count': 0})


@socketio.on('disconnect', namespace='/live')
def test_disconnect():
    print('Client disconnected')


@socketio.on('event', namespace='/live')
def test_message(message):
    emit('response',
         {'data': message['data']})


@socketio.on('livevideo', namespace='/live')
def test_live(message):
    print(message['data']['width'], message['data']['height'])
    # g.livestream.append(message['data'])


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_livestream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    socketio.run(app)
