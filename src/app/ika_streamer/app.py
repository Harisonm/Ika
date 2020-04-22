import os
import flask
import src.app.ika_streamer.api.routes.IkaStreamer

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.app.ika_streamer.api.routes.IkaStreamer.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()