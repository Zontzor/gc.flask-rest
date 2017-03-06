from gevent.wsgi import WSGIServer
import os.path

if os.path.exists('config.py'):
    from app import app
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
else:
    print("No config file, exiting...")
