# Importing required libraries
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.app.collect_mail.manager.CollectManager import CollectManager
from dotenv import load_dotenv
from pathlib import Path
import json
import csv
import os
import time

SERVICE_ACCOUNT = "resources/gcp_credential/service_account.json"
CLIENT_SECRET = "resources/gmail_credential/gmail_credentials.json"
SCHEMA = "default/app/utils/data_pipeline/collect_mail/resources/schema/gmail_fields.json"
PATH_SAVE = "a_collect_gmail/"
"""
Usage: Insert data in BigQuery into dataset
python -m default.app.utils.data_pipeline.collect_mail.AcollectMail
"""


def main():
    """
    Returns:
    """
    begin_time = time.time()
    env_path = Path('default/app/utils/data_pipeline/collect_mail/.env')

    name_file_dict = GmailDataFactory('dev').get_user().execute()
    name_file = name_file_dict['emailAddress'] + str(int(begin_time))
    name_user = name_file_dict['emailAddress']

    load_dotenv(dotenv_path=env_path)

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

    # Collect mail
    message_id = GmailDataFactory('dev').get_message_id('me',
                                                        include_spam_trash=True,
                                                        max_results=10000,
                                                        batch_using=True)

    reader = csv.mails = CollectManager('dev').collect_mail('me', message_id)

    # Save mail in Csv
    with open(PATH_SAVE + name_file + '.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)
        fc.writeheader()
        fc.writerows(reader)

if __name__ == '__main__':
    main()
