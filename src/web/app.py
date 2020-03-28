import os
import flask
import gevent
from gevent.pywsgi import WSGIServer
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import src.components.gmail_manager.tests.routes.TestGmailRoutes
import src.web.google_auth
import src.app.collect_mail.api.AcollectMailApi
import src.app.transform_mail.api.BtransformApi
import src.app.classification_mail.api.build_label
import src.app.classification_mail.routes.delete_label
import src.web.test.routes.test

app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.web.google_auth.app)
app.register_blueprint(src.components.gmail_manager.tests.routes.TestGmailRoutes.app)
app.register_blueprint(src.app.collect_mail.api.AcollectMailApi.app)
app.register_blueprint(src.app.transform_mail.api.BtransformApi.app)
app.register_blueprint(src.app.classification_mail.api.build_label.app)
app.register_blueprint(src.app.classification_mail.routes.delete_label.app)
app.register_blueprint(src.web.test.routes.test.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()

