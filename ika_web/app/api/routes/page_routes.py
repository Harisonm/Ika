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
    return flask.render_template("loading_page.html")
