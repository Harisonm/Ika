from components.big_query_manager.client.BigQueryClient import BigQueryClient
from components.cloud_storage_manager.client.CloudStorageClient import CloudStorageClient
from src.app.transform_mail.manager.TransformMailManager import TransformMmailManager
from src.components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
from dotenv import load_dotenv
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

    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    dataset_id_collect = os.getenv("DATASET_ID_COLLECT")
    table_id_collect = os.getenv("TABLE_ID_COLLECT") + name_user
    dataset_id_transform = os.getenv("DATASET_ID_TRANSFORM")
    table_id_transform = os.getenv("TABLE_ID_TRANSFORM") + name_user
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

    # Save mail in Csv
    with open(PATH_SAVE + name_file, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=fieldnames)
        fc.writeheader()
        fc.writerows(reader)

    # Send Csv into cloud storage
    object_name = PATH_SAVE + name_file
    gs_path = 'gs://' + bucket_id + '/' + object_name

    # Test 1 : Insert data into GS
    CloudStorageClient(SERVICE_ACCOUNT, bucket_id).buckets().insert(object_name)

    # From cloud storage insert data into big query
    BigQueryClient(SERVICE_ACCOUNT, project_id).job().load(dataset_id_transform, table_id_transform, gs_path, schema)
    return flask.redirect(flask.url_for('labelling.build_label_mail', name_file=name_file, code=302))
