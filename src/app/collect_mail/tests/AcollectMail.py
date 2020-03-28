from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from src.app.collect_mail.manager.CollectManager import CollectManager
import json
import csv
import os
import time

CLIENT_SECRET = os.environ.get("SCHEMA_COLLECT", default=False)
SCHEMA = os.environ.get("SCHEMA_COLLECT", default=False)
PATH_SAVE = os.environ.get("PATH_SAVE_COLLECT", default=False)


def main():
    begin_time = time.time()

    name_file_dict = GmailDataFactory('dev').get_user().execute()
    name_file = name_file_dict['emailAddress'] + str(int(begin_time))

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

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
