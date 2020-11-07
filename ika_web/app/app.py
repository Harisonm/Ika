import os
import ika_web.app.api.routes.page_routes
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from ika_web.app.api.database.db import initialize_db
from ika_web.app.api.resources import errors
from ika_web.app.api_spec import spec
from ika_web.app.api.routes.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL
from flask_mail import Mail
import re

app = Flask(__name__,
            template_folder="./web/templates",
            static_folder="./web/static")

app.config.from_envvar('ENV_FILE_LOCATION')
# app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mail = Mail(app)

from ika_web.app.api.routes.api_routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

MONGO_URI = os.environ.get("MONGO_URI", default=False)
MONGODB_SETTINGS = {
    'host': MONGO_URI
}

# with app.test_request_context():
#     # register all swagger documented functions here
#     for fn_name in app.view_functions:
#         if fn_name == 'static':
#             continue
#         print(f"Loading swagger docs for function: {fn_name}")
#         view_fn = app.view_functions[fn_name]
#         spec.path(view=view_fn)


# @app.route("/api/v1/swagger.json")
# def create_swagger_spec():
#     return jsonify(spec.to_dict())


initialize_db(app)
initialize_routes(api)

app.register_blueprint(ika_web.app.api.routes.page_routes.app)
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)