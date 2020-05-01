import os
import flask
import json
import requests
from flask import Flask, render_template, redirect, url_for, request, jsonify
app = flask.Blueprint("page", __name__)

@app.route("/")
def login_page():
    """
    Returns:
    """
    flask.flash("You were successfully logged in")

    return flask.render_template(
        "login_ika.html",
        redirect_url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/google/authorize",
        registrer=os.environ.get("FN_BASE_URI", default=False) + "/registrer"
    )

@app.route("/registrer", methods=['GET'])
def registrer():
    return flask.render_template("registrer.html")

@app.route("/add_registrer", methods=['GET','POST'])
def add_registrer():
    url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/signup"
    if request.method == 'POST':
        if request.form['password'] == request.form['comfirm_password']:
            myobj = {
                    'email':request.form['your_email'],
                    'password':request.form['password'],
                    'first_name':request.form['first_name'],
                    'last_name':request.form['last_name']
                    }
            x = requests.post(url, json=myobj)
        else:
            print('mdp diff')
            return flask.render_template("registrer.html")
        
    return flask.render_template("login_ika.html")


@app.route("/login_ika", methods=['GET','POST'])
def login_ika():
    url=os.environ.get("FN_BASE_URI", default=False) + "/api/v1/auth/login"
    url_test=os.environ.get("FN_BASE_URI", default=False) + "/loading_page"
    
    if request.method == 'GET':
            return render_template('login_ika.html')
        
    elif request.method == 'POST':
        myobj = {
        'email':request.form['email'],
        'password':request.form['pass'],
        }
        r = requests.post(url, json=myobj)
        data = r.json()
        print(data)
        
        
        return redirect("/api/v1/google/authorize")
        
    else:
        print('error')
    
    
@app.route("/home")
def home_page():
    """
    Returns:
    """
    return flask.render_template("home.html")


@app.route("/loading_page")
def loading_page():
    """
    Returns:
    """
    return flask.render_template("login_google.html")