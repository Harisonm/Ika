from googleapiclient import http

from default.components.cloud_storage_manager.manager.EntityManager import EntityManager

EXPORTING_EXTENTION = "NEWLINE_DELIMITED_JSON"
import uuid


class Buckets(EntityManager):

    def __init__(self, client, bucket_id):
        """Manager Data in/from Cloud Storage
        Args:
            self : Authorized BigQuery API service instance.
            client: Client Credentials Services
            bucket_id: Name of buckets
        Returns:
        """
        super(Buckets, self).__init__(client, bucket_id)
        self.__client = client
        self.__bucket_id = bucket_id

    def get_data(self):
        """Get a Data from Bucket Cloud Storage.
        Retrieves a list of objects matching the criteria. Try it now.
        In conjunction with the prefix filter,
        the use of the delimiter parameter allows the list method to operate like a directory listing,
        despite the object namespace being flat. For example, if delimiter were set to "/",
        then listing objects from a bucket that contains the objects
        "a/b", "a/c", "d", "e", "e/f" would return objects "d" and "e", and prefixes "a/" and "e/".

        The authenticated user must have READER permissions on the bucket.

        Args:
            self : Authorized BigQuery API service instance.
        Returns:
        """
        try:

            response = self.__client.objects().list(bucket=self.__bucket_id).execute()
            return response

        except Exception as exception:
            print(exception)

    def insert(self, file_path, mime_type='application/csv'):
        """Stores a new object and metadata. For tips on uploading to Cloud Storage, see this link :
            -   https://cloud.google.com/storage/docs/best-practices?hl=fr#uploading
            For examples of performing object uploads with different Cloud Storage tools and client libraries,
            see the Uploading Objects guide.
            This method supports an /upload URI and accepts uploaded media with the following characteristics:
                -   Maximum file size: 5 TB
                -   Accepted Media MIME types: */*
                -   The authenticated user must have WRITER permissions on the bucket.

        Note: Metadata-only requests are not allowed. To change an object's metadata, use either the update or patch methods.

        To provide a customer-supplied encryption key along with the object upload,
        use the headers listed on the Encryption page in your request.
        Args:
            self : Authorized Cloud Storage API service instance.
            file_path: Path of your File
            mime_type: Global description about your File
        Returns:

        """
        try:

            media = http.MediaFileUpload(file_path,
                                         mimetype=mime_type,
                                         resumable=True)
            response = self.__client.objects().insert(bucket=self.__bucket_id,
                                                      name=file_path,
                                                      media_body=media
                                                      ).execute()
            return response

        except Exception as exception:
            print(exception)
