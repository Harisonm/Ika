import flask
import google.oauth2.credentials
import googleapiclient.discovery
from src.web.google_auth import *

app = flask.Blueprint('test', __name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.insert',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.settings.basic',
          'https://www.googleapis.com/auth/gmail.settings.sharing']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'


@app.route('/test', methods=['GET', 'POST'])
def test_api_request():
    """

    Returns:

    """
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    gmail = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    mails = gmail.users().messages().list(
        userId='me', maxResults=10, includeSpamTrash=True).execute()

    # files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    # return files
    return flask.jsonify(**mails)
