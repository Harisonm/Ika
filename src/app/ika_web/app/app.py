import os
import flask
import src.app.ika_web.app.api.routes.google_auth
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.app.ika_web.app.api.database.db import initialize_db
from src.app.ika_web.app.api.routes.routes import initialize_routes

app = flask.Flask(__name__,
                  template_folder="./web/templates",
                  static_folder="./web/static")

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

app.register_blueprint(src.app.ika_web.app.api.routes.google_auth.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()
