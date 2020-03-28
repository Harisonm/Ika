import os
import flask
import gevent

app = flask.Flask(__name__, template_folder='./templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(components.o_auth2_web_server.google_auth.app)
app.register_blueprint(components.gmail_manager.tests.routes.TestGmailRoutes.app)
app.register_blueprint(app.utils.data_pipeline.collect_mail.api.AcollectMailApi.app)
app.register_blueprint(app.utils.data_pipeline.transform_mail.api.BtransformApi.app)
app.register_blueprint(app.classification_mail.api.build_label.app)
app.register_blueprint(app.classification_mail.routes.delete_label.app)
app.register_blueprint(components.o_auth2_web_server.test.routes.test.app)
app_server = gevent.pywsgi

