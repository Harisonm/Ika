from components.big_query_manager.client.BigQueryClient import BigQueryClient
from components.cloud_storage_manager.client.CloudStorageClient import CloudStorageClient
from components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from app.transform_mail.manager.TransformMailManager import TransformMmailManager
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import json
import os
import csv
import time
import sys

SERVICE_ACCOUNT = "resources/gcp_credential/service_account.json"
SCHEMA = "default/app/utils/data_pipeline/transform_mail/resources/schema/gmail_fields.json"
PATH_SAVE = "b_transform_gmail/"

"""
Usage:
python -m default.app.utils.data_pipeline.transform_mail.BtransformMail
"""


def main(name_file):
    begin_time = time.time()
    env_path = Path('default/app/utils/data_pipeline/transform_mail/.env')

    name_user_dict = GmailDataFactory('dev').get_user().execute()
    name_user = name_user_dict['emailAddress']

    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    dataset_id_collect = os.getenv("DATASET_ID_COLLECT")
    table_id_collect = os.getenv("TABLE_ID_COLLECT") + name_user
    dataset_id_transform = os.getenv("DATASET_ID_TRANSFORM")
    table_id_transform = os.getenv("TABLE_ID_TRANSFORM")
    bucket_id = os.getenv("BUCKET_ID")

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    fieldnames = []
    for field in schema['fields']:
        fieldnames.append(field['name'])

    infos_table = BigQueryClient(SERVICE_ACCOUNT, project_id).table().get(dataset_id_collect,
                                                                          table_id_collect)
    a_collect_gmail = BigQueryClient(SERVICE_ACCOUNT, project_id).table().get_data(dataset_id_collect,
                                                                                   table_id_collect,
                                                                                   len_table=infos_table['numRows'])

    reader = csv.mails_transform = TransformMmailManager(a_collect_gmail).transform_mail()
    print(type(reader))

    # Save mail in Csv
    with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)
        fc.writeheader()
        fc.writerows(reader)

    # Send Csv into cloud storage
    object_name = PATH_SAVE + name_file
    gs_path = 'gs://' + bucket_id + '/' + object_name
    print('csv ', time.time() - begin_time)
    # Test 1 : Insert data into GS
    CloudStorageClient(SERVICE_ACCOUNT, bucket_id).buckets().insert(object_name)

    # From cloud storage insert data into big query
    BigQueryClient(SERVICE_ACCOUNT, project_id).job().load(dataset_id_transform, table_id_transform, gs_path, schema)


if __name__ == '__main__':
    main(sys.argv[1])
