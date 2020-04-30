import os
import flask
import json
import requests
from flask import Flask, render_template, redirect, url_for, request
app = flask.Blueprint("page", __name__)

@app.route("/")
def login_page():
    """
    Returns:
    """
    flask.flash("You were successfully logged in")

    return flask.render_template(
        "index.html",
        redirect_url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/google/authorize",
        registrer=os.environ.get("FN_BASE_URI", default=False) + "/registrer"
    )

@app.route("/registrer", methods=['GET'])
def registrer():
    return flask.render_template("registrer.html")

@app.route("/add_registrer", methods=['GET', 'POST'])
def validate():
    url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/signup"
    if request.method == 'POST':
        form = request.form
        print(form)
        myobj = {
                'email':request.form['your_email'],
                'password':request.form['password'],
                }
        x = requests.post(url, json=myobj)
    return flask.render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/login"
    if request.method == 'POST':
        form = request.form
        myobj = {
        'email':request.form['email'],
        'password':request.form['pass'],
        }
        r = requests.post(url, json=myobj)
        data = r.json() 
        print(data)
    return flask.render_template("login.html") 
    
@app.route("/home")
def home_page():
    """
    Returns:
    """
    return flask.render_template("home.html", error=error)


@app.route("/loading_page")
def loading_page():
    """
    Returns:
    """
    return flask.render_template("login.html")