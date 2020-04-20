import os
import flask
import src.web.google_auth
import src.web.test.routes.test

app = flask.Flask(__name__, template_folder="./templates")
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.web.google_auth.app)
app.register_blueprint(src.web.test.routes.test.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()