import os
import flask
import src.web.app.routes.google_auth
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from src.web.app.database.db import initialize_db
from flask_restful import Api
from src.web.app.routes.routes import initialize_routes

app = flask.Flask(__name__, template_folder="./templates")

app.config.from_envvar('ENV_FILE_LOCATION')

app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/google-auth-bag'
}

initialize_db(app)
initialize_routes(api)

app.register_blueprint(src.web.app.routes.google_auth.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()
