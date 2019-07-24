from bs4 import BeautifulSoup
import base64
import bleach
import re
import unicodedata


class TransformMmailManager(object):
    def __init__(self, mail):
        """Get a Data from table in BigQuery
        Args:
            self : Authorized BigQuery API service instance.
            client:
            project_id:
        Returns:
        """
        self.__mail = mail
        self.__mails_collected = []

    def transform_mail(self):
        mail = {}
        self.__build_mail_from_collect()

        for data in self.__mails_collected:
            if data['body'] is not None:
                mail['idMail'] = data['idMail']
                mail['threadId'] = data['threadId']
                mail['historyId'] = data['historyId']
                mail['from'] = data['from']
                mail['to'] = data['to']
                mail['date'] = data['date']
                mail['labelIds'] = str((data['labelIds'])).replace('[', '').replace(']', '').replace('\'', '')
                mail['spam'] = 1 if 'SPAM' in data['labelIds'] else 0
                mail['body'] = self.__html_to_text(data['body'])

                mail['mimeType'] = data['mimeType']
                yield mail
            elif data['snippet'] is not None:
                mail['idMail'] = data['idMail']
                mail['threadId'] = data['threadId']
                mail['historyId'] = data['historyId']
                mail['from'] = data['from']
                mail['to'] = data['to']
                mail['date'] = data['date']
                mail['labelIds'] = str((data['labelIds'])).replace('[', '').replace(']', '').replace('\'', '')
                mail['spam'] = 1 if 'SPAM' in data['labelIds'] else 0
                mail['body'] = self.__html_to_text(data['snippet'])
                yield mail

    def __split_sender_mail(self):
        pass

    def __build_mail_from_collect(self):
        for row in self.__mail:
            self.__mails_collected.append({
                'idMail': row['f'][0]['v'],
                'threadId': row['f'][1]['v'],
                'historyId': row['f'][2]['v'],
                'labelIds': row['f'][3]['v'],
                'snippet': row['f'][4]['v'],
                'payloadPartId': row['f'][5]['v'],
                'payloadMimeType': row['f'][6]['v'],
                'deliveredTo': row['f'][7]['v'],
                'received': row['f'][8]['v'],
                'xGoogleSmtpSource': row['f'][9]['v'],
                'xReceived': row['f'][10]['v'],
                'arcMessageSignature': row['f'][11]['v'],
                'arcAuthenticationResults': row['f'][12]['v'],
                'returnPath': row['f'][13]['v'],
                'receivedSPF': row['f'][14]['v'],
                'authenticationResults': row['f'][15]['v'],
                'dKimsSignature': row['f'][16]['v'],
                'headersMessageId': row['f'][17]['v'],
                'mimeVersion': row['f'][18]['v'],
                'from': row['f'][19]['v'],
                'to': row['f'][20]['v'],
                'subject': row['f'][21]['v'],
                'date': row['f'][22]['v'],
                'headersListId': row['f'][23]['v'],
                'headersListUnsubscribe': row['f'][24]['v'],
                'precedence': row['f'][25]['v'],
                'xCsaComplaints': row['f'][26]['v'],
                'xMjMid': row['f'][27]['v'],
                'xMjMimeMessageStructure': row['f'][28]['v'],
                'feedbackId': row['f'][29]['v'],
                'contentType': row['f'][30]['v'],
                'size': row['f'][31]['v'],
                'body': row['f'][32]['v'],
                'mimeType': row['f'][33]['v']
            })

    @staticmethod
    def __split_sender(mail):
        part_sender = mail['sender']
        try:
            name_sender, mail_sender = part_sender.split('<')
            mail_sender = mail_sender.replace('>', '')
            yield name_sender, mail_sender

        except Exception as exception:
            print(exception)

    def __html_to_text(self, body):

        if body is not None:
            soup = BeautifulSoup(body, 'html.parser')
            text = soup.getText()  # getting text from html

            lines = [line.strip() for line in text.splitlines()]  # removing leading/trailing spaces
            chunks = [phrase.strip() for line in lines for phrase in line.split(' ')]  # breaking multi-headlines into
            # line each
            text = ' '.join([chunk for chunk in chunks])  # removing newlines
            # Using bleach
            clean_text = bleach.clean(text, strip=True)
            msg = self.remove_urls(clean_text)

        else:
            msg = ''
        return msg

    def remove_urls(self, v_text):
        v_text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', v_text, flags=re.MULTILINE)
        new_string = self.strip_accents(v_text.lower())
        new_string = new_string.replace('&gt', '')
        text = re.sub('<[^<]+?>', '', new_string)
        text1 = ' '.join([w for w in text.split() if ((len(w) > 3) and (len(w) < 23))])
        return text1

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
            text = str(text, 'utf-8')
        except (TypeError, NameError):  # unicode is a default on python 3
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ASCII', 'ignore')
        text = text.decode("utf-8")
        return str(text)
