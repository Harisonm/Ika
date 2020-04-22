# Importing required libraries
from src.app.ika_streamer.api.helper.GmailHelper import GmailDataFactory
from src.app.ika_streamer.api.models.CollecterModel import CollecterModel
from src.app.ika_streamer.api.database.mongo import mdb
import flask
import json
import csv
import os
import time

SCHEMA_TRANSFORM = os.environ.get("SCHEMA_TRANSFORM", default=False)
SCHEMA_COLLECT = os.environ.get("SCHEMA_COLLECT", default=False)
PATH_SAVE = os.environ.get("PATH_FILE", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)

"""
Usage: collect data from Gmail
GET host:port/collect/gmail/{name_file}

example : 
"""

app = flask.Blueprint("ika_streamer", __name__)

@app.route("/api/v1/ika_streamer", methods=["GET"])
def collect_mail():
    
    message_id = GmailDataFactory("prod").get_message_id(
        "me", include_spam_trash=False, max_results=25, batch_using=True
    )
    print(message_id)
    mycol = mdb["collect"]
    large_generator_handle = CollecterModel("prod",transform_flag=True).collect_mail("me", message_id)

    mycol.insert(large_generator_handle)

    return flask.redirect('/you_were_redirected',code=302)
    
@app.route("/you_were_redirected")
def redirected():
    return "You were redirected. Congrats :)!"


