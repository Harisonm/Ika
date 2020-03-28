from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.app.transform_mail.manager.TransformMailManager import TransformMmailManager
from pathlib import Path  # python3 only
import json
import os
import csv
import time
import sys

SCHEMA = os.environ.get("SCHEMA_TRANSFORM", default=False)
PATH_SAVE = os.environ.get("PATH_SAVE_TRANSFORM", default=False)
HOME_URI = os.environ.get("HOME_URI", default=False)

"""
Usage:
python -m default.app.utils.data_pipeline.transform_mail.BtransformMail
"""


def main(name_file):
    begin_time = time.time()
    env_path = Path('default/app/utils/data_pipeline/transform_mail/.env')

    name_user_dict = GmailDataFactory('dev').get_user().execute()
    name_user = name_user_dict['emailAddress']

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

    # reader = csv.mails_transform = TransformMmailManager(a_collect_gmail).transform_mail()
    # print(type(reader))
    #
    # # Save mail in Csv
    # with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
    #     fc = csv.DictWriter(output_file, fieldnames=fieldnames)
    #     fc.writeheader()
    #     fc.writerows(reader)


if __name__ == '__main__':
    main(sys.argv[1])
