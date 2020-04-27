import os
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from src.ika_web.app.api.database.models import Credential

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=False)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.settings.sharing",

]
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"

app = flask.Blueprint("google_auth", __name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = "REPLACE ME - this value is here as a placeholder."


@app.route("/authorize")
def authorize():
    """
    Returns:
    """
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=SCOPES
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for("google_auth.auth", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server app.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    flask.session["state"] = state

    return flask.redirect(authorization_url)


@app.route("/auth")
def auth():
    """
    Returns:
    """
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=None, state=state
    )
    flow.redirect_uri = flask.url_for("google_auth.auth", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credential = Credential(**credentials_to_dict(flow.credentials)).save()

    return flask.redirect("/loading_page")


@app.route("/revoke")
def revoke():
    """
    Returns:
    """
    if "credentials" not in flask.session:
        return (
                'You need to <a href="/authorize">authorize</a> before '
                + "testing the code to revoke credentials."
        )

    credentials = google.oauth2.credentials.Credentials(**flask.session["credentials"])

    revoke = requests.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == 200:
        return "Credentials successfully revoked."
    else:
        return "An error occurred."


@app.route("/clear")
def clear_credentials():
    """
    Returns:
    """
    if "credentials" in flask.session:
        del flask.session["credentials"]
    return "Credentials have been cleared.<br><br>" 


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
