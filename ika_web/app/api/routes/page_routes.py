import os
import flask
import json
import requests
import google_auth_oauthlib.flow
from flask import Flask, render_template, redirect, url_for, request, jsonify
from ika_web.app.api.database.models import Credential

app = flask.Blueprint("page", __name__)
os.environ.get("OAUTHLIB_INSECURE_TRANSPORT") 

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

# @app.route("/")
# def login_page():
#     """
#     login_page 
#     """
#     return flask.render_template("login_google.html")


@app.route("/", methods=['GET', 'POST'])
def login_ika():
    """
    login_ika [summary]

    Returns:
        [type]: [description]
    """
    url = os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/login"
    url_test = os.environ.get("FN_BASE_URI", default=False) + "/loading_page"

    if request.method == 'POST':
        myobj = {
            'email': request.form['email'],
            'password': request.form['pass'],
        }
        r = requests.post(url, json=myobj)
        data = r.json()
        print(data)
        if r.status_code == 200:
            return flask.render_template('login_google.html')

    elif request.method == 'GET':
        return flask.render_template('login_ika.html')


@app.route("/register", methods=['GET'])
def register():
    """
    registrer [summary]

    Returns:
        [type]: [description]
    """
    return flask.render_template("register.html")


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=False)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = os.environ.get("FN_BASE_URI", default=False) + "/oauth2callback"

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    """
    Returns:
    """
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session["state"]
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=False)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=SCOPES, state=state
    )
    flow.redirect_uri = os.environ.get("FN_BASE_URI", default=False) + "/oauth2callback"
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credential = Credential(**credentials_to_dict(flow.credentials)).save()
    return flask.redirect(flask.url_for('page.loading_page'))


def credentials_to_dict(credentials):
    return {
        "token": credentials.get('token'),
        "refresh_token": credentials.get('refresh_token'),
        "token_uri": credentials.get('token_uri'),
        "client_id": credentials.get('client_id'),
        "client_secret": credentials.get('client_secret'),
        "scopes": credentials.get('scopes'),
    }

@app.route("/add_register", methods=['GET', 'POST'])
def add_register():
    """
    add_register [summary]

    Returns:
        [type]: [description]
    """
    url = os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/signup"
    if request.method == 'POST':
        if request.form['password'] == request.form['comfirm_password']:
            myobj = {
                'email': request.form['your_email'],
                'password': request.form['password'],
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name']
            }
            x = requests.post(url, json=myobj)
        else:
            print('mdp diff')
            return flask.render_template("registrer.html")

    return flask.render_template("login_ika.html")


@app.route("/home")
def home_page():
    """
    home_page [summary]

    Returns:
        [type]: [description]
    """
    return flask.render_template("home.html")


@app.route("/loading_page")
def loading_page():
    """
    loading_page [summary]

    Returns:
        [type]: [description]
    """
    return flask.render_template("login_google.html")
