import os
import src.ika_web.app.api.routes.page_routes
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mail import Mail
from src.ika_web.app.api.database.db import initialize_db
from src.ika_web.app.api.resources import errors

app = Flask(__name__,
                  template_folder="./web/templates",
                  static_folder="./web/static")


app.config.from_envvar('ENV_FILE_LOCATION')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

mail = Mail(app)

from src.ika_web.app.api.routes.api_routes import initialize_routes
api = Api(app, errors=errors)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/google-auth-bag'
}

initialize_db(app)
initialize_routes(api)

app.register_blueprint(src.ika_web.app.api.routes.page_routes.app)