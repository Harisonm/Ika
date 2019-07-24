import os
import flask
import gevent
from gevent import pywsgi

from default.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
import default.components.gmail_manager.tests.routes.TestGmailRoutes
import default.components.o_auth2_web_server.test.routes.test
import default.components.o_auth2_web_server.google_auth
import default.apps.utils.data_pipeline.collect_mail.api.AcollectMailApi
import default.apps.utils.data_pipeline.transform_mail.api.BtransformApi
import default.apps.classification_mail.api.build_label
import default.apps.classification_mail.routes.delete_label


app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(default.components.o_auth2_web_server.google_auth.app)
app.register_blueprint(default.components.gmail_manager.tests.routes.TestGmailRoutes.app)
app.register_blueprint(default.apps.utils.data_pipeline.collect_mail.api.AcollectMailApi.app)
app.register_blueprint(default.apps.utils.data_pipeline.transform_mail.api.BtransformApi.app)
app.register_blueprint(default.apps.classification_mail.api.build_label.app)
app.register_blueprint(default.apps.classification_mail.routes.delete_label.app)
app.register_blueprint(default.components.o_auth2_web_server.test.routes.test.app)
app_server = gevent.pywsgi

