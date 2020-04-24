# Importing required libraries
from __future__ import print_function
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from src.app.ika_streamer.api.helper.database.mongo import mdb
# from src.web import google_auth
from apiclient import errors
import pickle
import os.path
import random
import google.oauth2.credentials
import googleapiclient.discovery
import flask
from pathlib import Path  # python3 only

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
                messages.extend(response["messages"])

            if batch_using:
                while "nextPageToken" in response:
                    page_token = response["nextPageToken"]
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
                    messages.extend(response["messages"])
            return messages

        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def delete_label_from_id(self, user_id, label_id):
        """Delete a label.

        Args:
          self.__service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          label_id: string id of the label.
        """
        try:
            self.__service.users().labels().delete(
                userId=user_id, id=label_id
            ).execute()
            print("Label with id: %s deleted successfully." % label_id)
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def found_label_id(self):
        """Found label Id from label name.
        Returns:

        """

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
            print(messages)
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

    def send_mail(self, user_id, message_body):
        """Send Mail

        Args:
          self : Authorized GMail API service instance.
          user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
            The special value "me"
          can be used to indicate the authenticated user.
          message_body: the body of the message to be sent

        Returns:
        A Message.
        """
        try:
            message = (
                self.__service.users()
                .messages()
                .send(userId=user_id, body=message_body)
                .execute()
            )
            return message

        except errors.HttpError as error:
            print(error)

    def get_spam_mails(self, user_id, label_id):
        spams = self.__service.users().labels().get(user_id, label_id)
        return spams

    def get_user(self):
        user = self.__service.users().getProfile(userId="me")
        return user

    """
    PART OF LABEL
    """

    def create_label(
        self,
        user_id,
        name_label="",
        label_list_visibility="labelShow",
        message_list_visibility="show",
    ):
        """function to creates a new label

        Args:
            self : Authorized GMail API service instance.
            user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"
            name_label: label_name
            label_list_visibility: visibility of label
            message_list_visibility

        Returns:
            labels (list): return mail label.
        """
        background_color = [
            "#000000e",
            "#434343",
            "#666666",
            "#999999",
            "#cccccc",
            "#efefef",
            "#f3f3f3",
            "#ffffff",
            "#fb4c2f",
            "#ffad47",
            "#fad165",
            "#16a766",
            "#43d692",
            "#4a86e8",
            "#a479e2",
            "#f691b3",
            "#f6c5be",
            "#ffe6c7",
            "#fef1d1",
            "#b9e4d0",
            "#c6f3de",
            "#c9daf8",
            "#e4d7f5",
            "#fcdee8",
            "#efa093",
            "#ffd6a2",
            "#fce8b3",
            "#89d3b2",
            "#a0eac9",
            "#a4c2f4",
            "#d0bcf1",
            "#fbc8d9",
            "#e66550",
            "#ffbc6b",
            "#fcda83",
            "#44b984",
            "#68dfa9",
            "#6d9eeb",
            "#b694e8",
            "#f7a7c0",
            "#cc3a21",
            "#eaa041",
            "#f2c960",
            "#149e60",
            "#3dc789",
            "#3c78d8",
            "#8e63ce",
            "#e07798",
            "#ac2b16",
            "#cf8933",
            "#d5ae49",
            "#0b804b",
            "#2a9c68",
            "#285bac",
            "#653e9b",
            "#b65775",
            "#822111",
            "#a46a21",
            "#aa8831",
            "#076239",
            "#1a764d",
            "#1c4587",
            "#41236d",
            "#83334c",
        ]

        text_color = [
            "#000000",
            "#434343",
            "#666666",
            "#999999",
            "#cccccc",
            "#efefef",
            "#f3f3f3",
            "#ffffff",
            "#fb4c2f",
            "#ffad47",
            "#fad165",
            "#16a766",
            "#43d692",
            "#4a86e8",
            "#a479e2",
            "#f691b3",
            "#f6c5be",
            "#ffe6c7",
            "#fef1d1",
            "#b9e4d0",
            "#c6f3de",
            "#c9daf8",
            "#e4d7f5",
            "#fcdee8",
            "#efa093",
            "#ffd6a2",
            "#fce8b3",
            "#89d3b2",
            "#a0eac9",
            "#a4c2f4",
            "#d0bcf1",
            "#fbc8d9",
            "#e66550",
            "#ffbc6b",
            "#fcda83",
            "#44b984",
            "#68dfa9",
            "#6d9eeb",
            "#b694e8",
            "#f7a7c0",
            "#cc3a21",
            "#eaa041",
            "#f2c960",
            "#149e60",
            "#3dc789",
            "#3c78d8",
            "#8e63ce",
            "#e07798",
            "#ac2b16",
            "#cf8933",
            "#d5ae49",
            "#0b804b",
            "#2a9c68",
            "#285bac",
            "#653e9b",
            "#b65775",
            "#822111",
            "#a46a21",
            "#aa8831",
            "#076239",
            "#1a764d",
            "#1c4587",
            "#41236d",
            "#83334c",
        ]
        try:
            body = {
                "labelListVisibility": label_list_visibility,
                "messageListVisibility": message_list_visibility,
                "name": name_label,
                "color": {
                    "backgroundColor": random.choice(background_color),
                    "textColor": random.choice(text_color),
                },
            }
            label = (
                self.__service.users()
                .labels()
                .create(userId=user_id, body=body)
                .execute()
            )
            return label
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def get_label_ids(self, user_id, labels_in):
        """function to list of label Id using in users Gmail

        Args:

            self : Authorized GMail API service instance.
            user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"
            labels_in:

        Returns:
            labels (list): return mail label.
        """
        try:
            result = []
            results = self.__service.users().labels().list(userId=user_id).execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
            for label_in in labels_in:
                for label in labels:
                    if label["name"] == label_in:
                        result.append(label["id"])
                        break
            return result

        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def list_label(self, user_id):
        """function to list of label using in users Gmail

        Args:
            self : Authorized GMail API service instance.
            user_id (str): The user's email address. The special value me can be used to indicate the authenticated user.
                The special value "me"

        Returns:
            labels (list): return mail label.
        """
        try:
            results = self.__service.users().labels().list(userId=user_id).execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
            else:
                print("Labels:")
                for label in labels:
                    print(label["name"])

            return labels
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

    def get_label(self, user_id, mail_id):
        """Creates a new label within user's mailbox, also prints Label ID.

        Args:
            self: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            mail_id: Mail ID
        Returns:
            Created Label.
        """
        try:
            labels = (
                self.__service.users()
                .labels()
                .get(userId=user_id, id=mail_id)
                .execute()
            )
            return labels
        except errors.HttpError as error:
            print("An error occurred: %s" % error)

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

    # @staticmethod
    # def createMessage(sender, to, subject, message):
    #     message = MIMEText(message)
    #     message['to'] = to
    #     message['from'] = sender
    #     message['subject'] = subject
    #     return {'raw': base64.urlsafe_b64encode(message.as_string())}

    # def create_draft(self, user_id, message):
    #     try:
    #         message = (self.__service.users().drafts().create(userId=user_id,
    #                                                         body=message).execute())
    #         return message
    #     except errors.HttpError as error:
    #         print(error)
