import os
import flask

from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory

app = flask.Blueprint('google_gmail', __name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)


@app.route('/gmail/test', methods=['GET'])
def test_api_request():
    mails_id = GmailDataFactory('prod').get_message_id('me',
                                                       include_spam_trash=True,
                                                       max_results=10)

    return flask.jsonify(results=mails_id)
