flask-socketio-video-stream
===========================

It's an attempt to capture a videostream with getUserMedia(), send it to server using websockets, then play it in a video control.

It barely works and the framerate is very slow.

Try it with:
```
virtualenv env --no-site-packages
source env/bin/activate
pip install -r requirements.txt
gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -b 0.0.0.0:4000 livestream:app
```

Then, point to http://127.0.0.1:4000
