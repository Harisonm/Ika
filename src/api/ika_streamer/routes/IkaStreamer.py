# Importing required libraries
from src.helper.GmailHelper import GmailDataFactory
from src.api.ika_streamer.models.CollecterModel import CollecterModel
from src.api.ika_streamer.models.TransformerModel import TransformerModel
from src.api.ika_streamer.database.models import Mail
from src.api.ika_streamer.models.StreamArray import StreamArray
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

@app.route("/collect", methods=["GET"])
def collect_mail():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")
    begin_time = time.time()

    name_file_dict = GmailDataFactory("prod").get_user().execute()
    name_file = name_file_dict["emailAddress"] + str(int(begin_time))

    # name_user = re.search(r'(.*[^@]?)@', name_file_dict['emailAddress'])
    # name_user = str(name_user.group(0).replace('@', '')).replace('.', '_')


    schema = {}
    with open(SCHEMA_COLLECT) as json_file:
        schema["fields"] = json.load(json_file)

    fieldnames = []
    for field in schema["fields"]:
        fieldnames.append(field["name"])
    
    message_id = GmailDataFactory("prod").get_message_id(
        "me", include_spam_trash=False, max_results=25, batch_using=True
    )
    print(message_id)
    
    #Write the contents to file:
    with open(PATH_SAVE + 'streamed_write.json', 'w') as outfile:
        large_generator_handle = CollecterModel("prod").collect_mail("me", message_id)
        stream_array = StreamArray(large_generator_handle)
        for chunk in json.JSONEncoder().iterencode(stream_array):
            print('Writing chunk: ',chunk)
            outfile.write(chunk)
    
    # reader_clean = csv.mails_transform = TransformerModel(reader).transform_mail()
    # next(reader_clean)
    # print(reader_clean)
    # for mail in mails:
    #     mail =  Mail(**mail).save()

    # return {'id': str(id)}, 200

    return flask.redirect('/you_were_redirected',code=302)
    
@app.route("/you_were_redirected")
def redirected():
    return "You were redirected. Congrats :)!"


