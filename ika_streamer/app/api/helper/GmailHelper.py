# Importing required libraries
from __future__ import print_function
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
# from app.api.helper.database.mongo import mdb
from app.api.database.mongo import mdb
# from web import google_auth
from apiclient import errors
import pickle
import os.path
import random
import google.oauth2.credentials
import googleapiclient.discovery

# CLIENT_SECRET_PATH = os.environ.get("CLIENT_SECRET", default=False)
CLIENT_SECRET_PATH="resources/client_secret_localhost.json"
"""
Reading GMAIL using API GMAIL for Python
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.insert",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.metadata",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.settings.sharing",
]
PATH_TOKEN = "resources/gmail_credential/"
API_SERVICE_NAME = "gmail"
API_VERSION = "v1"


class GmailDataFactory(object):
    def __init__(self, env):
        """function to init GmailDataFactory Class .
        Args:

        Returns:
            None
        """
        self.__service = (
            self.__build_service(CLIENT_SECRET_PATH)
            if env == "dev"
            else self.build_gmail_credential_api_v1()
        )

    @staticmethod
    def __build_service(client_secret):
        """Function to Build service using to call API Gmail.
            The file token.pickle stores the user's access and refresh tokens, and is
            created automatically when the authorization flow completes for the first time.
            Args:
                client_secret: credential to call GMAIL API.

            Returns:
            Return service building.
        """
        credentials = None

        if os.path.exists(PATH_TOKEN + "token.pickle"):
            with open(PATH_TOKEN + "token.pickle", "rb") as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(PATH_TOKEN + "token.pickle", "wb") as token:
                pickle.dump(credentials, token)

        service = build("gmail", "v1", credentials=credentials)
        print("SERVICE", service)
        return service

    @staticmethod
    def build_gmail_credential_api_v1():
        """Build Credential to API version 1
        Args :

        Returns :
            Return service building.
        """
        # flask.session["credentials"] = google_auth.credentials_to_dict(credentials)
        
        mycol = dict(mdb["credential"].find_one())
        del mycol["_id"]
        
        credentials = google.oauth2.credentials.Credentials(**mycol)

        service = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials
        )

        return service

    def get_message_id(
        self, user_id, include_spam_trash=False, max_results=10, batch_using=False
    ):
        """Get a Message and return List of Id Message.
        Args:
            self : Authorized GMail API service instance.
            user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"
            include_spam_trash (bool): Include messages from SPAM and TRASH in the results. (Default: false)
            max_results (int): Maximum number of messages to return.
            can be used to indicate the authenticated user.
            batch_using(bool): if Flag False -> Take nextPageToken else True -> Take by batch
        Returns:
          results : A List of mail_id, consisting of data from Message.
        """
        try:
            messages = []
            response = (
                self.__service.users()
                .messages()
                .list(
                    userId=user_id,
                    maxResults=max_results,
                    includeSpamTrash=include_spam_trash,
                )
                .execute()
            )
            if "messages" in response:
                messages.extend(response.get("messages"))

            if batch_using:
                while "nextPageToken" in response:
                    page_token = response.get("nextPageToken")
                    response = (
                        self.__service.users()
                        .messages()
                        .list(
                            userId=user_id,
                            maxResults=max_results,
                            pageToken=page_token,
                            includeSpamTrash=include_spam_trash,
                        )
                        .execute()
                    )
                    messages.extend(response.get("messages"))
            return messages

        except errors.HttpError as error:
            print("An error occurred: %s" % error)


    def get_message(self, user_id, mail_id, format="full"):
        """Get a Message with given ID.

        Args:
          self : Authorized GMail API service instance.
          user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"
          mail_id(str): The ID of the Message required.
          format(str) : The format to return the message in.
            Acceptable values are:
            "full": Returns the full email message data with body content parsed in the payload field;
            the raw field is not used. (default)
            "metadata": Returns only email message ID, labels, and email headers.
            "minimal": Returns only email message ID and labels; does not return the email headers, body, or payload.
            "raw": Returns the full email message data with body content in the raw field as a base64url encoded string;
            the payload field is not used.
        Returns:
          A Message.
        """
        try:
            messages = (
                self.__service.users()
                .messages()
                .get(userId=user_id, id=mail_id, format=format)
                .execute()
            )
            return messages

        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def get_message_by_thread(self, user_id, max_results=10, include_spam_trash=False):
        """Get a Message with given Thread ID.

            Args:
              self : Authorized GMail API service instance.
               user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"
              max_results:
              include_spam_trash:
              format:

            Returns:
            mail_box : A Message.
            """
        try:
            threads = (
                self.__service.users()
                .threads()
                .list(
                    userId=user_id,
                    maxResults=max_results,
                    includeSpamTrash=include_spam_trash,
                )
                .execute()
                .get("threads", [])
            )
            for thread in threads:
                messages = (
                    self.__service.users()
                    .threads()
                    .get(userId=user_id, id=thread["id"])
                    .execute()
                )
                return messages

        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def get_spam_mails(self, user_id, label_id):
        spams = self.__service.users().labels().get(user_id, label_id)
        return spams

    def get_user(self):
        user = self.__service.users().getProfile(userId="me")
        return user

    """
    PART OF LABEL
    """

    def modify_message(self, user_id, mail_id, mail_labels):

        """Modify the Labels on the given Message.

        Args:
            self: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            mail_id: The id of the message required.
            mail_labels: The change in labels.

        Returns:
            Modified message, containing updated labelIds, id and threadId.
        """
        try:
            message = (
                self.__service.users()
                .messages()
                .modify(userId=user_id, id=mail_id, body=mail_labels)
                .execute()
            )

            label_ids = message["labelIds"]

            print("Message ID: %s - With Label IDs %s" % (mail_id, label_ids))
            return message
        except errors.HttpError as error:
            print("An error occurred: %s" % error)
