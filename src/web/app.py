import os
import flask
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import src.components.gmail_manager.tests.routes.TestGmailRoutes
import src.web.google_auth
import src.api.collect_mail.routes.AcollectMailApi
import src.api.transform_mail.routes.BtransformApi
import src.api.classification_mail.routes.build_label
import src.api.classification_mail.routes.delete_label
import src.web.test.routes.test

app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.web.google_auth.app)
app.register_blueprint(src.components.gmail_manager.tests.routes.TestGmailRoutes.app)
app.register_blueprint(src.api.collect_mail.routes.AcollectMailApi.app)
app.register_blueprint(src.api.transform_mail.routes.BtransformApi.app)
app.register_blueprint(src.api.classification_mail.routes.build_label.app)
app.register_blueprint(src.api.classification_mail.routes.delete_label.app)
app.register_blueprint(src.web.test.routes.test.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()

