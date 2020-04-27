import os
import flask
import requests

app = flask.Blueprint("page", __name__)

@app.route("/")
def login_page():
    """
    Returns:
    """
    flask.flash("You were successfully logged in")

    return flask.render_template(
        "login.html",
        redirect_url=os.environ.get("FN_BASE_URI", default=False) + "/authorize",
    )
    
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
    return flask.render_template("loading_page.html")