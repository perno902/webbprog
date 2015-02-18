from Twidder import app
import eventlet
from gevent.wsgi import WSGIServer
app.run(debug=True)

#http_server = WSGIServer(('', 5000), app)
#http_server.serve_forever()