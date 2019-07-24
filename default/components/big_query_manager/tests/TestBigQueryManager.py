from default.components.big_query_manager.client.BigQueryClient import BigQueryClient
from dotenv import load_dotenv
from pathlib import Path  # python3 only
import os

SERVICE_ACCOUNT = "resources/big_query_credential/service_account.json"

"""
Usage: list table in dataset
python -m default.components.big_query_manager.tests.TestBigQueryManager
"""

if __name__ == "__main__":
    env_path = Path('default/components/big_query_manager/.env')

    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    dataset_id = os.getenv("DATASET_ID")
    table_id = os.getenv("TABLE_ID")

    data = BigQueryClient(SERVICE_ACCOUNT, project_id).table().get_data(dataset_id, table_id)
    for e in data:
        for i in e:
            print(i)

