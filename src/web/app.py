import os
import flask
import src.helper.routes.TestGmailRoutes
import src.web.google_auth
import src.api.collecter_mail.routes.AcollectMailApi
import src.api.transformer_mail.routes.BtransformApi
import src.api.classifier_mail.routes.build_label
import src.api.classifier_mail.routes.delete_label
import src.web.test.routes.test

app = flask.Flask(__name__, template_folder="./templates")
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(src.web.google_auth.app)
app.register_blueprint(src.helper.routes.TestGmailRoutes.app)
app.register_blueprint(src.api.collecter_mail.routes.AcollectMailApi.app)
app.register_blueprint(src.api.transformer_mail.routes.BtransformApi.app)
app.register_blueprint(src.api.classifier_mail.routes.build_label.app)
app.register_blueprint(src.api.classifier_mail.routes.delete_label.app)
app.register_blueprint(src.web.test.routes.test.app)
# http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
# http_server.serve_forever()
