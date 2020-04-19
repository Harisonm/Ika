import os
import flask
import src.helper.routes.TestGmailRoutes
import src.web.google_auth
import src.api.ika_streamer.routes.IkaStreamer
import src.web.test.routes.test
from src.api.ika_streamer.database.db import initialize_db
from src.api.ika_streamer.database.models import Mail

app = flask.Flask(__name__, template_folder="./templates")
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb://localhost/mail-bag'
# }
# initialize_db(app)

app.register_blueprint(src.web.google_auth.app)
app.register_blueprint(src.helper.routes.TestGmailRoutes.app)
app.register_blueprint(src.api.ika_streamer.routes.IkaStreamer.app)
app.register_blueprint(src.web.test.routes.test.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()