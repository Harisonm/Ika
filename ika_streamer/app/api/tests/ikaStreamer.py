# Importing required libraries
from ikamail.GmailHelper import GmailHelper
from api.ika_streamer.models.CollecterModel import CollecterModel
from api.ika_streamer.models.TransformerModel import TransformerModel

import flask
import json
import csv
import os
import time
import sys

SCHEMA = os.environ.get("SCHEMA_TRANSFORM", default=False)
PATH_SAVE = os.environ.get("PATH_FILE", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)

"""
Usage: collect data from Gmail
GET host:port/collect/gmail/{name_file}

example : 
"""


def main():
    begin_time = time.time()

    name_file_dict = GmailHelper("dev").get_user().execute()
    name_file = name_file_dict["emailAddress"] + str(int(begin_time))

    schema = {}
    with open(SCHEMA) as json_file:
        schema["fields"] = json.load(json_file)

    fieldnames = []
    for field in schema["fields"]:
        fieldnames.append(field["name"])
        
    message_id = GmailHelper("dev").get_message_id(
        "me", include_spam_trash=False, max_results=10000, batch_using=True
    )
    print(message_id)

    reader = CollecterModel("dev").collect_mail("me", message_id)
    print(reader)
    
    reader_clean = csv.mails_transform = TransformerModel(reader).transform_mail()
    print(reader_clean)
    # Save mail in Csv
    with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)
        fc.writeheader()
        fc.writerows(reader_clean)


if __name__ == "__main__":
    main()