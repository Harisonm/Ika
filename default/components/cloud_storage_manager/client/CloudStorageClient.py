from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from googleapiclient.discovery import build
from default.components.cloud_storage_manager.entity.Buckets import Buckets


SCOPE = "https://www.googleapis.com/auth/devstorage.full_control"


class CloudStorageClient(object):

    def __init__(self, service_account, bucket_id=None):
        """Initialize Class CloudStorageClient with client_ID
        Args:
            self : Authorized Cloud Storage API service instance.
        Returns:
        """
        self.__bucket_id = bucket_id
        self.__buckets = Buckets
        self.__client = self.__set_client_credential(service_account, SCOPE, 'storage', 'v1')

    @staticmethod
    def __set_client_credential(json_key_file, api_scopes, api_name, api_version):
        """Set client credential to Cloud Storage and build HTTPS call
        Args:
            json_key_file (object): Authorized Cloud Storage API service instance.
            api_scopes (str):
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
            http=credential.authorize(httplib2.Http()),
        )
        return client

    def buckets(self):
        """Using Buckets class building from Parent class
        Args:
            self : Authorized BigQuery API service instance.
        Returns:
            table (object): return table object
        """
        bucket = Buckets(self.__client, self.__bucket_id)
        return bucket


