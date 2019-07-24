from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from googleapiclient.discovery import build
from default.components.big_query_manager.entity.Dataset import Dataset
from default.components.big_query_manager.entity.Table import Table
from default.components.big_query_manager.entity.Job import Job

SCOPE = "https://www.googleapis.com/auth/bigquery"


class BigQueryClient(object):

    def __init__(self, service_account, project_id=None):
        """Initialize Class BigQueryClient with project_id, dataset_id, table_id and client_ID
        Args:
            self : Authorized BigQuery API service instance.
            service_account: service_account.json using to do call API
            project_id (str): Name of project_id in BigQuery

        Attributes:
            project_id  (str): name of project ID using in Google Cloud Plateform
            self.__dataset (object): instantiation of Dataset Class
            self.__table (object): instantiation of Table Class
            self.__job (object): instantiation of Job Class
            self.__client (object): instantiation of client object
        Returns: None
        """
        self.__project_id = project_id
        self.__dataset = Dataset
        self.__table = Table
        self.__job = Job
        self.__client = self.__set_client_credential(service_account, SCOPE, 'bigquery', 'v2')

    @staticmethod
    def __set_client_credential(json_key_file, api_scopes, api_name, api_version):
        """Set client credential to Big Query and build HTTPS call
        Args:
            json_key_file (object): Authorized BigQuery API service instance.
            api_scopes (str): Url scope Using to call API
            api_name (str): API name Used
            api_version (str): API version used
        Returns:
        """
        credential = ServiceAccountCredentials.from_json_keyfile_name(
            filename=json_key_file,
            scopes=api_scopes
        )
        client = build(
            api_name,
            api_version,
            http=credential.authorize(httplib2.Http())
        )
        return client

    def dataset(self):
        """Using Dataset class building from Parent class
        Args:
            self : Authorized BigQuery API service instance.
        Returns:
            dataset (object): return dataset object
        """
        dataset = Dataset(self.__client, self.__project_id)
        return dataset

    def table(self):
        """Using Table class building from Parent class
        Args:
            self : Authorized BigQuery API service instance.
        Returns:
            table (object): return table object
        """
        table = Table(self.__client, self.__project_id)
        return table

    def job(self):
        """Using Job class building from Parent class
        Args:
            self : Authorized BigQuery API service instance.
        Returns:
            table (object): return table object
        """
        job = Job(self.__client, self.__project_id)
        return job
