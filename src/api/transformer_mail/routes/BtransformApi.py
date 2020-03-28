from src.helper.GmailHelper import GmailDataFactory
from src.api.transformer_mail.manager.TransformMailManager import TransformMailManager
import json
import os
import flask
import re
import pandas as pd

SCHEMA = os.environ.get("SCHEMA_TRANSFORM", default=False)
PATH_SAVE = os.environ.get("PATH_FILE", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)

"""
Usage: transform data mails
GET host:port/transform/{name_file}
"""
app = flask.Blueprint("b_transform_gmail", __name__)


@app.route("/transform/<name_file>", methods=["GET", "POST"])
def transform_mail(name_file):
    # labelling_uri = os.environ.get("FN_BASE_URI", default=False) + '/labelling/' + name_file

    name_user_dict = GmailDataFactory("prod").get_user().execute()
    name_user = re.search(r"(.*[^@]?)@", name_user_dict["emailAddress"])
    name_user = str(name_user.group(0).replace("@", "")).replace(".", "_")

    schema = {}
    with open(SCHEMA) as json_file:
        schema["fields"] = json.load(json_file)

    fieldnames = []
    for field in schema["fields"]:
        fieldnames.append(field["name"])

    df = pd.read_csv(
        os.environ.get("PATH_FILE", default=False) + name_file,
        encoding="utf8",
        sep=",",
    )
    print(df)
    reader = csv.mails_transform = TransformMailManager(df).transform_mail()
    #
    # # Save mail in Csv
    # with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
    #     fc = csv.DictWriter(output_file, fieldnames=fieldnames)
    #     fc.writeheader()
    #     fc.writerows(reader)

    # return flask.redirect(flask.url_for('labelling.build_label_mail', name_file=name_file, code=302))
