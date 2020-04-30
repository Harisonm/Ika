import os
import flask
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
    if request.method == 'POST':
        form = request.form
        print(form)
        print('ok')
        # date = request.myform['date']
        # title = request.myform['blog_title']
        # post = request.myform['blog_main']
        # post_entry = models.BlogPost(date = date, title = title, post = post)
        # db.session.add(post_entry)
        # db.session.commit()
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
    return flask.render_template("loading_page.html")