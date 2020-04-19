from bs4 import BeautifulSoup
import base64
import bleach
import re
import unicodedata


class TransformerModel(object):
    def __init__(self, mail):
        """Get a Data from table in BigQuery
        Args:
            self : Authorized BigQuery API service instance.
            client:
            project_id:
        Returns:
        """
        self.__mails_collected = mail

    def transform_mail(self):
        mail = {}
        
        if self.__mails_collected["body"] is not None:
            mail["idMail"] = self.__mails_collected["idMail"]
            mail["threadId"] = self.__mails_collected["threadId"]
            mail["historyId"] = self.__mails_collected["historyId"]
            mail["from"] = self.__mails_collected["from"]
            mail["to"] = self.__mails_collected["to"]
            mail["date"] = self.__mails_collected["date"]
            mail["labelIds"] = (
                str((self.__mails_collected["labelIds"]))
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            mail["spam"] = 1 if "SPAM" in self.__mails_collected["labelIds"] else 0
            mail["body"] = self.__html_to_text(self.__mails_collected["body"])

            mail["mimeType"] = self.__mails_collected["mimeType"]
            return mail
        elif self.__mails_collected["snippet"] is not None:
            mail["idMail"] = self.__mails_collected["idMail"]
            mail["threadId"] = self.__mails_collected["threadId"]
            mail["historyId"] = self.__mails_collected["historyId"]
            mail["from"] = self.__mails_collected["from"]
            mail["to"] = self.__mails_collected["to"]
            mail["date"] = self.__mails_collected["date"]
            mail["labelIds"] = (
                str((self.__mails_collected["labelIds"]))
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            mail["spam"] = 1 if "SPAM" in self.__mails_collected["labelIds"] else 0
            mail["body"] = self.__html_to_text(self.__mails_collected["snippet"])
            return mail

    def __split_sender_mail(self):
        pass
    
    @staticmethod
    def __split_sender(mail):
        part_sender = mail["sender"]
        try:
            name_sender, mail_sender = part_sender.split("<")
            mail_sender = mail_sender.replace(">", "")
            return name_sender, mail_sender

        except Exception as exception:
            print(exception)

    def __html_to_text(self, body):

        if body is not None:
            soup = BeautifulSoup(body, "html.parser")
            text = soup.getText()  # getting text from html

            lines = [
                line.strip() for line in text.splitlines()
            ]  # removing leading/trailing spaces
            chunks = [
                phrase.strip() for line in lines for phrase in line.split(" ")
            ]  # breaking multi-headlines into
            # line each
            text = " ".join([chunk for chunk in chunks])  # removing newlines
            # Using bleach
            clean_text = bleach.clean(text, strip=True)
            msg = self.remove_urls(clean_text)

        else:
            msg = ""
        return msg

    def remove_urls(self, v_text):
        v_text = re.sub(
            r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b",
            "",
            v_text,
            flags=re.MULTILINE,
        )
        new_string = self.strip_accents(v_text.lower())
        new_string = new_string.replace("&gt", "")
        text = re.sub("<[^<]+?>", "", new_string)
        url = " ".join([w for w in text.split() if ((len(w) > 3) and (len(w) < 23))])
        return url

    @staticmethod
    def strip_accents(text):
        """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        try:
            text = str(text, "utf-8")
        except (TypeError, NameError):  # unicode is a default on python 3
            pass
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ASCII", "ignore")
        text = text.decode("utf-8")
        return str(text)
