from components.gmail_manager.factory.GmailDataFactory import GmailDataFactory
# from google.cloud.exceptions import ServiceUnavailable
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from traceback import print_exc
import concurrent.futures
import base64

CLIENT_SECRET = "default/app/utils/data_pipeline/collect_mail/resources/credentials/gmail_credentials.json"


# CLIENT_SECRET = "default/components/big_query_manager/resources/credentiel_big_query_neomail.json"


class CollectManager(object):

    def __init__(self, env):
        """function to init GmailDataFactory Class .
        Args:
            client_secret: credential to call GMAIL API.

        Returns:
            None
        """
        self.__service = GmailDataFactory(env)

    def build_data(self, **kwargs):
        """
        We get a dictionary. Now reading values for the key 'messages'

        Args:
          self : Authorized GMail API service instance.
          final_list: list to store gmail data
          **kwargs(keyworded): list of data from call API Gmail

        Returns:
           list, The final_list will have dictionary in the following format:
            {
                'idMail' (str): '16a1c9f4f066141e',
                'threadId' (str):   '16a1c9f4f066141e',
                'historyId' (str):  '1977184',
                'labelIds' (str):   '['CATEGORY_PROMOTIONS', 'UNREAD', 'SPAM']',
                'snippet' (str):    'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet'',
                'payloadPartId' (str):  '',
                'payloadMimeType' (str):    'multipart/alternative',
                'received' (str):   'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
                'xGoogleSmtpSource' (str): 'APXvYqwgNTPd8hREorTSPfcoi3HH+hHZYbdgYM5OC83dujJCHDSEANqwsygNOm2/RGHgU1e1awvO',
                'xReceived' (str): 'by 2002:a17:902:1621:: with SMTP id',
                'arcMessageSignature' (str):    'i=1; a=rsa-sha256; c=relaxed/relaxed',
                'arcAuthenticationResults' (str):'i=1; mx.google.com;'
                'returnPath' (str):'1974469'    Investir - Morning Letter <newsletter@newsinv.lesechos.fr>,
                'receivedSPF' (str):'1974469'   'pass (google.com: domain of 232',
                'authenticationResults' (str):'mx.google.com;',
                'dKimsSignature' (str):'v=1; a=rsa-sha256; c=',
                'headersMessageId' (str):'  <483b1eb3.AGgAACiDSnMAASm_j0QAAGVfN8EAAP-Oa4IAF2BzAAk3swBcrD-9@mailjet.com>'
                'mimeVersion' (str):'1.0',
                'from' (str):'Name <name@domaine-mail.com>' ,
                'to' (str):'Name <name@domaine-mail.com>',
                'subject' (str):'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
                'date' (str):'Tue, 23 Apr 2019 18:30:46 +0200',
                'headersListId' (str):  '<newsletter.newsinv.lesechos.fr.koms-x7k23.mj>,
                'headersListUnsubscribe' (str): '<mailto:unsub-483b1eb3.koms.xhg2pu1y7j29@bnc3.mailjet.com>',
                'precedence' (str):'bulk'
                'xCsaComplaints' (str):'whitelist-complaints@eco.de',
                'xMjMid' (str):'AGgAACiDSnMAASm_j0',
                'xMjMimeMessageStructure' (str):'no-related',
                'feedbackId' (str):'161165.604083:MJ',
                'contentType' (str):'multipart/related; type="text/html',
                'size' (str):'585655',
                'body' (str):'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
                'mimeType' (str):'text/plain;text/html;'
                
                
                
            }
           The dictionary can be exported as a .csv or into a database
        """
        temp_dict = {}
        for key, mail in kwargs.items():
            temp_tab = self.get_headers_value(mail['payload']['headers'])

            # First part of mail
            try:
                temp_dict['idMail'] = mail['id']
            except KeyError:
                temp_dict['idMail'] = ''

            try:
                temp_dict['threadId'] = mail['threadId']
            except KeyError:
                temp_dict['threadId'] = ''
            try:
                temp_dict['historyId'] = mail['historyId']
            except KeyError:
                temp_dict['historyId'] = ''
            try:
                temp_dict['labelIds'] = str(mail['labelIds'])
            except KeyError:
                temp_dict['labelIds'] = ''
            try:
                temp_dict['snippet'] = mail['snippet']
            except KeyError:
                temp_dict['snippet'] = ''
            try:
                temp_dict['payloadPartId'] = mail['payload']['partId']
            except KeyError:
                temp_dict['payloadPartId'] = ''
            try:
                temp_dict['payloadMimeType'] = mail['payload']['mimeType']
            except KeyError:
                temp_dict['payloadMimeType'] = ''

            # seconde partie
            try:
                temp_dict['deliveredTo'] = temp_tab['Delivered-To']
            except KeyError:
                temp_dict['deliveredTo'] = ''
            try:
                temp_dict['received'] = temp_tab['Received']
            except KeyError:
                temp_dict['received'] = ''
            try:
                temp_dict['xGoogleSmtpSource'] = temp_tab['X-Google-Smtp-Source']
            except KeyError:
                temp_dict['xGoogleSmtpSource'] = ''
            try:
                temp_dict['xReceived'] = temp_tab['X-Received']
            except KeyError:
                temp_dict['xReceived'] = ''
            try:
                temp_dict['arcMessageSignature'] = temp_tab['ARC-Message-Signature']
            except KeyError:
                temp_dict['arcMessageSignature'] = ''
            try:
                temp_dict['arcAuthenticationResults'] = temp_tab['ARC-Authentication-Results']
            except KeyError:
                temp_dict['arcAuthenticationResults'] = ''
            try:
                temp_dict['returnPath'] = temp_tab['Return-Path']
            except KeyError:
                temp_dict['returnPath'] = ''
            try:
                temp_dict['receivedSPF'] = temp_tab['Received-SPF']
            except KeyError:
                temp_dict['receivedSPF'] = ''
            try:
                temp_dict['authenticationResults'] = temp_tab['Authentication-Results']
            except KeyError:
                temp_dict['authenticationResults'] = ''
            try:
                temp_dict['dKimsSignature'] = temp_tab['DKIM-Signature']
            except KeyError:
                temp_dict['dKimsSignature'] = ''
            try:
                temp_dict['headersMessageId'] = temp_tab['Message-Id']
            except KeyError:
                temp_dict['headersMessageId'] = ''
            try:
                temp_dict['mimeVersion'] = temp_tab['MIME-Version']
            except KeyError:
                temp_dict['mimeVersion'] = ''
            try:
                temp_dict['from'] = temp_tab['From']
            except KeyError:
                temp_dict['from'] = ''
            try:
                temp_dict['to'] = temp_tab['To']
            except KeyError:
                temp_dict['to'] = ''
            try:
                temp_dict['subject'] = temp_tab['Subject']
            except KeyError:
                temp_dict['subject'] = ''
            try:
                temp_dict['date'] = temp_tab['Date']
            except KeyError:
                temp_dict['date'] = ''
            try:
                temp_dict['headersListId'] = temp_tab['List-Id']
            except KeyError:
                temp_dict['headersListId'] = ''
            try:
                temp_dict['headersListUnsubscribe'] = temp_tab['List-Unsubscribe']
            except KeyError:
                temp_dict['headersListUnsubscribe'] = ''
            try:
                temp_dict['precedence'] = temp_tab['Precedence']
            except KeyError:
                temp_dict['precedence'] = ''
            try:
                temp_dict['xCsaComplaints'] = temp_tab['X-CSA-Complaints']
            except KeyError:
                temp_dict['xCsaComplaints'] = ''
            try:
                temp_dict['xMjMid'] = temp_tab['X-MJ-Mid']
            except KeyError:
                temp_dict['xMjMid'] = ''
            try:
                temp_dict['xMjMimeMessageStructure'] = temp_tab['X-MJ-MIMEMessageStructure']
            except KeyError:
                temp_dict['xMjMimeMessageStructure'] = ''
            try:
                temp_dict['feedbackId'] = temp_tab['Feedback-Id']
            except KeyError:
                temp_dict['feedbackId'] = ''
            try:
                temp_dict['contentType'] = temp_tab['Content-Type']
            except KeyError:
                temp_dict['contentType'] = ''

            # third part of mail
            try:
                if 'parts' in mail['payload']:
                    payload_parts = self.get_part(mail['payload']['parts'])
                    temp_dict['size'] = payload_parts['size'] if 'size' in payload_parts else ''
                    temp_dict['body'] = self.__transform_mail_body(
                        payload_parts['body']) if 'body' in payload_parts else ''
                    temp_dict['mimeType'] = str(payload_parts['mimeType']) if 'mimeType' in payload_parts else ''

                elif 'body' in mail['payload']:
                    temp_dict['size'] = mail['payload']['size'] if 'size' in mail['payload'] else ''
                    temp_dict['body'] = self.__transform_mail_body(mail['payload']['body']['data']) if 'body' in mail[
                        'payload'] else ''
                    temp_dict['mimeType'] = mail['payload']['mimeType'] if 'mimeType' in mail['payload'] else ''
                else:
                    temp_dict['size'] = ''
                    temp_dict['body'] = ''
                    temp_dict['mimeType'] = ''
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
            return temp_dict

    @staticmethod
    def __transform_mail_body(mail):
        try:
            text = base64.urlsafe_b64decode(mail).decode("UTF-8")
        except KeyError:
            text = ''
        return str(text)

    @staticmethod
    def get_part(mail):
        """function extract data from payload parts.
        Args:
            mail (list): mail data to extract data.

        Returns:
            list, The list will have dictionary in the following format:
            {
            'size' (int): 0,
            'body' (str): 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
            'mimeType' (str): 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet'
            }
        """
        parts_conc = {'size': 0, 'body': '', 'mimeType': ''}
        for one in mail:
            parts_conc['size'] += one['body']['size'] if 'size' in one['body'] else 0
            parts_conc['body'] += one['body']['data'] + ';' if 'data' in one['body'] else ''
            parts_conc['mimeType'] += one['mimeType'] + ';' if 'mimeType' in one else ''
        return parts_conc

    @staticmethod
    def get_headers_value(mail):
        """function to extract value data from headers.
        Args:
            mail (list): mail data to extract data.

        Returns:
            list, The list will have dictionary in the following format:
            {
            'name' (str): 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
            }
        """
        temp_dict = {}
        try:
            for one in mail:  # getting the Subject
                temp_dict[one['name']] = one['value']
            return temp_dict
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

    def collect_mail(self, user_id, message_id):
        """function collect data from list send by API Gmail.
        Args:
            user_id :
            message_id :

        Returns:
            list, The list will have dictionary in the following format:
            {
            'name' (str): 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
            ...
            'name' (str): 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
            }
        """
        print("Total  messages collect in inbox: ", str(len(message_id)))

        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            future_results = [
                executor.submit(self.build_data, mails=(self.__service.get_message(user_id, mail['id'], format='full'))) for
                mail in message_id]
            print(future_results)
            for future in future_results:
                try:
                    yield future.result()
                except:
                    print_exc()
