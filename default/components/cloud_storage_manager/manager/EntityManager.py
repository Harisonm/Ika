from abc import ABCMeta, abstractmethod
# from google.cloud.exceptions import ServiceUnavailable
import tenacity as tn
import time


class EntityManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, client=None, bucket_id=None):
        """Get a Data from table in BigQuery
        Args:
            self : Authorized CloudStorage API service instance.
            client:
            project_id:
        Returns:
        """
        self.__client = client
        self.__bucket_id = bucket_id
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
            api_version="v1",
            **kwargs
        )
