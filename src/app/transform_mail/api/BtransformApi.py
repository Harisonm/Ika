from src.app.transform_mail.manager.TransformMailManager import TransformMmailManager
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from pathlib import Path  # python3 only
import json
import os
import csv
import flask
import re

SERVICE_ACCOUNT = os.environ.get("SERVICE_ACCOUNT_GCP", default=False) 
SCHEMA = "default/app/utils/data_pipeline/transform_mail/resources/schema/gmail_fields.json"
PATH_SAVE = "b_transform_gmail/"
HOME_URI = '/home'
"""
Usage: transform data mails
GET host:port/transform/{name_file}
"""
app = flask.Blueprint('b_transform_gmail', __name__)


@app.route('/transform/<name_file>', methods=['GET', 'POST'])
def transform_mail(name_file):

    env_path = Path('default/app/utils/data_pipeline/transform_mail/.env')

    # labelling_uri = os.environ.get("FN_BASE_URI", default=False) + '/labelling/' + name_file

    name_user_dict = GmailDataFactory('prod').get_user().execute()
    name_user = re.search(r'(.*[^@]?)@', name_user_dict['emailAddress'])
    name_user = str(name_user.group(0).replace('@', '')).replace('.', '_')

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

    # reader = csv.mails_transform = TransformMmailManager(a_collect_gmail).transform_mail()
    #
    # # Save mail in Csv
    # with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
    #     fc = csv.DictWriter(output_file, fieldnames=fieldnames)
    #     fc.writeheader()
    #     fc.writerows(reader)

    return flask.redirect(flask.url_for('labelling.build_label_mail', name_file=name_file, code=302))
