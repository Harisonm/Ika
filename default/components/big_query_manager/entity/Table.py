from default.components.big_query_manager.manager.EntityManager import EntityManager

EXPORTING_EXTENTION = "NEWLINE_DELIMITED_JSON"
import uuid


class Table(EntityManager):

    def __init__(self, client, project_id):
        """Initialize Class Table to call API regarding Table APIs
        Args:
            self : Authorized BigQuery API service instance.
            client: Client using to call API
            project_id: project_id from Google Cloud Plateform

        Attributes:
            self.__self.__client (object):
            self.__project_id (str):
        Returns:
        """
        super(Table, self).__init__(client, project_id)
        self.__client = client
        self.__project_id = project_id
        self.__num_rows = 0

    def list(self, dataset_id):
        """Lists all tables in the specified dataset. Requires the READER dataset role.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
        Returns:
          A List of
        """
        try:
            request = self.__client.tables().list(projectId=self.__project_id, datasetId=dataset_id)
            response = super(Table, self)._execute_methods(request)
            return [data["tableReference"]["tableId"] for data in response["tables"]]
        except Exception as exception:
            print(exception)

    def get(self, dataset_id, table_id):
        """Gets the specified table resource by table ID. This method does not return the data in the table,
        it only returns the table resource, which describes the structure of this table.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
        Returns:
          A List of
        """
        try:
            request = self.__client.tables().get(projectId=self.__project_id, datasetId=dataset_id, tableId=table_id)
            response = super(Table, self)._execute_methods(request)
            return response
        except Exception as exception:
            print(exception)

    def delete(self, dataset_id, table_id):
        """Deletes the table specified by tableId from the dataset.
        If the table contains data, all the data will be deleted.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
        Returns:
          A List of
        """
        try:
            request = self.__client.tables().delete(projectId=self.__project_id, datasetId=dataset_id,

                                                    tableId=table_id)
            response = super(Table, self)._execute_methods(request)
            return response
        except Exception as exception:
            print(exception)

    def insert_all(self, dataset_id, table_id, json_objects):
        """Streams data into BigQuery one record at a time without needing to run a load job.
        A few minor differences between these 2 APIs:
            (1) InsertAllRequest.kind has default value "bigquery#tableDataInsertAllRequest" in the Apiary definition.
                But proto3 doesn't support string literal default value for string. Fortunately we don't really check that field anyway.
            (2) boolean value 'skipInvalidRows' and 'ignoreUnknownValues' can be unset in our existing system. In proto3,
                they are default to false. Fortunately the existing behavior treats unset as false by default.
                But this does restrict us to stick with the existing default behavior.
            (3) Unlike Apiary, there's no way to provide customized http error reason string.
                Since we can still return the same http code, this shouldn't be much trouble.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
            json_objects:
        Returns:
          A List of
        """
        data = {
            "kind": "bigquery#tableDataInsertAllRequest",
            "rows": [{"json": json_object} for json_object in json_objects]
        }
        try:
            request = self.__client.tabledata().insertAll(projectId=self.__project_id,
                                                          datasetId=dataset_id,
                                                          tableId=table_id,
                                                          body=data)
            response = super(Table, self)._call_methods(
                "POST",
                request,
                data=data)
            return response

        except Exception as exception:
            print(exception)

    def get_data(self, dataset_id, table_id, max_results=200, index_start=0, len_table=0):
        """Get a Data from table in BigQuery, tabledata.list the content of a table in rows.
        Retrieves table data from a specified set of rows.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
            max_results:
            index_start:
            len_table:
        Returns:
          A List of
        """
        try:
            mail = []
            current_index = 0

            response = self.__client.tabledata().list(projectId=self.__project_id,
                                                      datasetId=dataset_id,
                                                      tableId=table_id,
                                                      startIndex=index_start,
                                                      maxResults=max_results).execute()

            mail.extend(response['rows'])
            if int(len_table) > max_results:
                index_end = int(len_table) + max_results
                current_index += max_results

                while current_index != index_end:
                    response = self.__client.tabledata().list(projectId=self.__project_id,
                                                              datasetId=dataset_id,
                                                              tableId=table_id,
                                                              startIndex=current_index,
                                                              maxResults=max_results).execute()
                    print(response)
                    mail.extend(response['rows'])
                    current_index += max_results

                    if index_end < current_index + max_results:
                        response = self.__client.tabledata().list(projectId=self.__project_id,
                                                                  datasetId=dataset_id,
                                                                  tableId=table_id,
                                                                  startIndex=index_end - current_index,
                                                                  maxResults=max_results).execute()
                        mail.extend(response['rows'])
                        current_index = index_end
            return mail

        except Exception as exception:
            print(exception)

    def insert(self, dataset_id, table_id, data_objects, schema):
        """Insert Data into Big Query. Creates a new, empty table in the dataset if table specified is not exist.
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id:
            table_id:
            data_objects:
            schema:
        Returns:
          A List of
        """
        response = self.__client.tables().list(projectId=self.__project_id,
                                               datasetId=dataset_id).execute()

        table_exists = [row['tableReference']['tableId'] for row in response['tables'] if
                        row['tableReference']['tableId'] == table_id]
        try:
            if not table_exists:
                body = {
                    'tableReference': {
                        'tableId': table_id,
                        'projectId': self.__project_id,
                        'datasetId': dataset_id
                    },
                    'schema': schema
                }
                # Creates a new, empty table in the dataset.
                self.__client.tables().insert(projectId=self.__project_id,
                                              datasetId=dataset_id,
                                              body=body).execute()

            # with table created, now we can stream the data
            # to do so we'll use the tabledata().insertall() function.
            body = {
                'rows': [
                    {
                        'json': data_objects,
                        'insertId': str(uuid.uuid4())
                    }
                ]
            }
            self.__client.tabledata().insertAll(projectId=self.__project_id,
                                                datasetId=dataset_id,
                                                tableId=table_id,
                                                body=body).execute(num_retries=5)

        except Exception as exception:
            print(exception)
