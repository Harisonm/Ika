import os
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask_restful import Resource
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

class AuthorizeGoogle(Resource):
# @app.route("/authorize")
    def get(self):
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
        flow.redirect_uri = os.environ.get("FN_BASE_URI", default=False) + "/api/v1/google/authentification"

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

class AuthentificationGoogle(Resource):
# @app.route("/auth")
    def get(self):
        """
        Returns:
        """
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = flask.session["state"]

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET, scopes=None, state=state
        )
        flow.redirect_uri = os.environ.get("FN_BASE_URI", default=False) + "/api/v1/google/authentification"

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)

        credential = Credential(**self.credentials_to_dict(flow.credentials)).save()

        return flask.redirect("/loading_page")

    def credentials_to_dict(self,credentials):
        return {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
