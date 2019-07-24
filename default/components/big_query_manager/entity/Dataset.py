from default.components.big_query_manager.manager.EntityManager import EntityManager


class Dataset(EntityManager):

    def __init__(self, client, project_id):
        """Initialize Class Dataset to call API regarding dataset APIs
        Args:
            self : Authorized BigQuery API service instance.
            client: Client using to call API
            project_id: project_id from Google Cloud Plateform

        Attributes:
            self.__self.__client (object):
            self.__project_id (str):
        Returns:
        """
        super(Dataset, self).__init__(client, project_id)
        self.__client = client
        self.__project_id = project_id

    def create(self, dataset_id, location="EU"):
        """Creates a new empty dataset in Big Query
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id (str): Name of Dataset will create
            location (str): Location of dataset
        Returns:
        """
        body = {
            "datasetReference": {
                "datasetId": dataset_id
            },
            "location": location
        }
        try:
            request = self.__client.datasets().insert(projectId=self.__project_id, body=body)
            response = super(Dataset, self)._execute_methods(request)
            return response
        except Exception as exception:
            print(exception)

    def list(self):
        """Lists all datasets in the specified project to which the user has been granted the READER dataset role.
        Args:
            self : Authorized BigQuery API service instance.
        Returns:
        """
        try:
            request = self.__client.datasets().list(projectId=self.__project_id)
            response = super(Dataset, self)._execute_methods(request)
            return [data["datasetReference"]["datasetId"] for data in response["datasets"]]
        except Exception as exception:
            print(exception)

    def delete(self, dataset_id):
        """Deletes the dataset specified by the datasetId value. Before you can delete a dataset,
        you must delete all its tables, either manually or by specifying deleteContents.
        Immediately after deletion, you can create another dataset with the same name.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
        Returns:
        """
        try:
            request = self.__client.datasets().delete(projectId=self.__project_id, datasetId=dataset_id,
                                                      deleteContents=True)
            response = super(Dataset, self)._execute_methods(request)
            return response
        except Exception as exception:
            print(exception)
