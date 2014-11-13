flask-socketio-video-stream
===========================

It's an attempt to capture a videostream with getUserMedia(), send it to server using websockets, then play it in a <video> control.

It works but the framerate is very low

Try it with:
```
virtualenv env --no-site-packages
source env/bin/activate
pip install -r requirements.txt
gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -w 4 -b 0.0.0.0:4000 livestream:app
```