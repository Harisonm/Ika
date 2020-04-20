import os
import flask
import src.web.app.resources.google_auth
from src.web.database.db import initialize_db

app = flask.Flask(__name__, template_folder="./templates")
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/google-auth-bag'
}

initialize_db(app)

app.register_blueprint(src.web.app.resources.google_auth.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()