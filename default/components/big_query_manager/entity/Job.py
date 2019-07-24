from default.components.big_query_manager.manager.EntityManager import EntityManager

EXPORTING_EXTENTION_JSON = "NEWLINE_DELIMITED_JSON"


class Job(EntityManager):

    def __init__(self, client, project_id):
        """Initialize Class Job to call API regarding Job APIs
        Args:
            self : Authorized BigQuery API service instance.
            client: Client using to call API
            project_id: project_id from Google Cloud Plateform

        Attributes:
            self.__self.__client (object):
            self.__project_id (str):
        Returns:
        """
        super(Job, self).__init__(client, project_id)
        self.__client = client
        self.__project_id = project_id

    def query_lautcher(self, dataset_id, table_id, location="EU", max_results=1000):
        """Class methods are using to Build SQL Query into BQ and get Result from Big Query API
        Args:
            self : Authorized BigQuery API service instance.
            dataset_id (str):
            table_id (str):
            location (str):
            max_results (str):

        Returns:
        """
        data = []
        fields = []

        query_sql = "select * from {dataset_id}.{table_id}".format(dataset_id=dataset_id,
                                                                   table_id=table_id,
                                                                   maxResults=max_results)
        body = {"query": query_sql,
                "location": location}

        try:
            request = self.__client.jobs().query(projectId=self.__project_id,
                                                 body=body)
            response = super(Job, self)._execute_methods(request)
            data.extend(response['rows'])
            fields.append(response['schema'])

            return fields, data

        except Exception as exception:
            print(exception)

    def load(self, dataset_id, table_id, gs_path, table_infos):
        """Starts a new asynchronous job. Requires the Can View project role.
                This method supports an /upload URI and accepts uploaded media with the following characteristics:
                Maximum file size: For more information, see quota policy.
                Accepted Media MIME types: */*
                This method returns immediately.
            You must call jobs.get() and examine the job status to learn when the job is complete.
            You include one and only one of the following child properties in your job resource.
            The child property that you include defines the type of job it is.
            This method create Table in BigQuery by tables().insert() if table is not exist.

        Args:
            self : Authorized BigQuery API service instance.
            dataset_id (str): dataset name using BigQuery
            table_id (str): table name using to BigQuery
            gs_path (str): Google Storage Path using to store Data
            table_infos (object): Information about File to store

        Returns:
        """
        partition_field = table_infos.get("timePartitioning", None)
        content = {
            "kind": "bigquery#job",
            "configuration": {
                "load": {
                    "sourceUris": [gs_path],
                    "destinationTable": {
                        "projectId": self.__project_id,
                        "datasetId": dataset_id,
                        "tableId": table_id
                    },
                    "schema": {
                        "fields": table_infos["fields"]
                    },
                    "writeDisposition": "WRITE_TRUNCATE",
                    "allowQuotedNewlines": True,
                    "Autodetect": True,
                    "skipLeadingRows": 1,
                    "FieldDelimiter": ",",
                    "NullMarker": "",
                    "encoding": "UTF-8"
                }
            }
        }

        if partition_field is not None and partition_field.get("field", None) is not None:
            content["configuration"]["load"]["timePartitioning"] = {
                "field": partition_field["field"],
                "type": "DAY"
            }
        elif partition_field is not None and partition_field.get("field", None) is None:
            content["configuration"]["load"]["timePartitioning"] = {
                "type": "DAY"
            }

        try:
            response = self.__client.tables().list(projectId=self.__project_id,
                                                   datasetId=dataset_id).execute()

            table_exists = [row['tableReference']['tableId'] for row in response['tables'] if
                            row['tableReference']['tableId'] == table_id]

            if not table_exists:
                body = {
                    'tableReference': {
                        'tableId': table_id,
                        'projectId': self.__project_id,
                        'datasetId': dataset_id
                    },
                    'schema': table_infos
                }
                # Creates a new, empty table in the dataset.
                self.__client.tables().insert(projectId=self.__project_id,
                                              datasetId=dataset_id,
                                              body=body).execute()

            # Insert Data from Cloud Storage to BiqQuery
            request = self.__client.jobs().insert(projectId=self.__project_id,
                                                  body=content)

            response = super(Job, self)._execute_methods(request)

            job_id = response['jobReference']['jobId']

            job_result = super(Job, self)._check_results(job_id, "load",
                                                         dataset_id,
                                                         table_id)
            return job_result
        except Exception as exception:
            print(exception)
