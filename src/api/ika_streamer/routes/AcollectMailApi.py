# # Importing required libraries
# from src.helper.GmailHelper import GmailDataFactory
# from src.api.collecter_mail.manager.CollectManager import CollectManager
# import flask
# import json
# import csv
# import os
# import time

# PATH_SAVE = os.environ.get("PATH_FILE", default=False)
# SCHEMA = os.environ.get("SCHEMA_COLLECT", default=False)

# """
# Usage: collect data from Gmail
# GET host:port/collect/gmail/{name_file}

# example : 
# """

# app = flask.Blueprint("a_collect_gmail", __name__)


# @app.route("/collect", methods=["GET"])
# def collect_mail():
#     if "credentials" not in flask.session:
#         return flask.redirect("authorize")
#     begin_time = time.time()

#     name_file_dict = GmailDataFactory("prod").get_user().execute()
#     name_file = name_file_dict["emailAddress"] + str(int(begin_time))

#     # name_user = re.search(r'(.*[^@]?)@', name_file_dict['emailAddress'])
#     # name_user = str(name_user.group(0).replace('@', '')).replace('.', '_')

#     name_file_csv = name_file + ".csv"

#     schema = {}
#     with open(SCHEMA) as json_file:
#         schema["fields"] = json.load(json_file)

#     fieldnames = []
#     for field in schema["fields"]:
#         fieldnames.append(field["name"])

#     # Collect mail
#     message_id = GmailDataFactory("prod").get_message_id(
#         "me", include_spam_trash=False, max_results=25, batch_using=True
#     )
#     print(message_id)

#     reader = csv.mails = CollectManager("prod").collect_mail("me", message_id)
#     print(reader)
#     # Save mail in Csv
#     with open(
#         PATH_SAVE + name_file + ".csv", "w", encoding="utf8", newline=""
#     ) as output_file:
#         fc = csv.DictWriter(output_file, fieldnames=fieldnames)
#         fc.writeheader()
#         fc.writerows(reader)
 
#     return flask.redirect(flask.url_for("b_transform_gmail.transformer_mail", name_file=name_file_csv, code=302))
#     # return flask.redirect(flask.url_for('labelling.build_label_mail', name_file=name_file, code=302))
