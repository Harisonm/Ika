from abc import ABCMeta, abstractmethod
# from google.cloud.exceptions import ServiceUnavailable
import tenacity as tn
import time


class EntityManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, client=None, project_id=None):
        """Mother Class to Initiate
        Args:
            self : Authorized BigQuery API service instance.
            client (:obj:`int`, optional):
            project_id (str):
        Returns:
        """
        self.__client = client
        self.__project_id = project_id
        self._time_out_seconds = 3600

    @staticmethod
    def _execute_methods(request):
        """Method using to execute Build the calling API's Methods in Google Cloud Discovery
        Args:
            self : Authorized BigQuery API service instance.
            request:
        Returns:
        """
        return request.execute()

    @tn.retry(
        wait=tn.wait_random_exponential(multiplier=1, max=60),
        retry=tn.retry_if_exception_type(),
        stop=tn.stop_after_attempt(5))
    def _call_methods(self, http_verb, url, **kwargs):
        """Method using to Call  API's Methods in Google Cloud Discovery
        Args:
            self : Authorized Cloud Storage API service instance.
            http_verb:
            url:
            **kwargs:
        Returns:
        """
        return self.__client.api_request(
            http_verb,
            url,
            api_version="v2",
            **kwargs
        )

    def _check_results(self, job_id, job_type, dataset_id, table_id):
        """check_job_results : methods to check if execution jobs is good gone
        Args:
            self : Authorized BigQuery API service instance.
            job_id (str):
            job_type (object): Type of Job : Dataset Jobs, Table Jobs or General Jobs
            dataset_id (str):
            table_id (str):
        Returns:
        """
        request = self.__client.jobs().get(projectId=self.__project_id, jobId=job_id)
        response = self._execute_methods(request)
        start_time = time.time()
        duration = 0
        while response["status"]["state"] != "DONE" and (duration <= self._time_out_seconds):
            time.sleep(1)
            response = self.__client.jobs().get(projectId=self.__project_id, jobId=job_id)
            response = self._execute_methods(response)
            duration = time.time() - start_time

        if duration > self._time_out_seconds and response["status"]["state"] != "DONE":
            raise Exception("Time out %dsec exceeded for this current job" % self._time_out_seconds)

        try:
            print(response["status"]["errorResult"])
            print("\tERROR %s: %s.%s " % (job_type, dataset_id, table_id))
            return response["status"]["errorResult"]
        except KeyError:
            print("\tSUCCESS %s: %s.%s " % (job_type, dataset_id, table_id))
            return "\t {statistics}".format(statistics=response["statistics"])
