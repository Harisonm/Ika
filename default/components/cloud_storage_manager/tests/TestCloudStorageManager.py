from default.components.big_query_manager.client.BigQueryClient import BigQueryClient
from default.components.cloud_storage_manager.client.CloudStorageClient import CloudStorageClient
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os
import json
import time

SERVICE_ACCOUNT = "resources/cloud_storage_credential/service_account.json"
SCHEMA = "default/components/cloud_storage_manager/resources/schema/gmail_transform_fields.json"

"""
Usage: list Data from Cloud storage
python -m default.components.cloud_storage_manager.tests.TestCloudStorageManager
"""

if __name__ == "__main__":
    begin_time = time.time()

    env_path = Path('default/components/cloud_storage_manager/.env')

    load_dotenv(dotenv_path=env_path)
    bucket_id = os.getenv("BUCKET_ID")
    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("DATASET_ID")
    table_id = os.getenv("TABLE_ID")

    object_name = "b_transform_gmail/gmail_transform_manitra.csv"
    gs_path = 'gs://' + bucket_id + '/' + object_name

    schema = {}
    with open(SCHEMA) as json_file:
        schema['fields'] = json.load(json_file)

    # Test 1 : Insert data into GS
    gs_rep = CloudStorageClient(SERVICE_ACCOUNT, bucket_id).buckets().insert(object_name)
    print(gs_rep)

    bq_rep = BigQueryClient(SERVICE_ACCOUNT, project_id).job().load(dataset_id, table_id, gs_path, schema)

    # Test 2 : List data from GS
    # data = CloudStorageClient(SERVICE_ACCOUNT, bucket_id).buckets().get_data()
    # print(data)

    y = time.time() - begin_time
    print(time.strftime('%M # %S ', time.localtime()))
    print(y)
