# Importing required libraries
from src.helper.GmailHelper import GmailDataFactory
import os

# Creating a storage.JSON file with authentication details
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=False)

# if you using Gmail API from Google Cloud Plateform

"""
This script does the following:
- Go to GMail inbox
- Find and read all messages
- Extract details (Date, Sender, Subject, Snippet, Body) and decrypt them by beautiful soup
- Stock all message in list and print them
"""

"""
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret_localhost.json.dist should be saved in the same client as this file
"""

"""
Usage: Here you can test all of API Gmail
python -m default.components.gmail_manager.tests.TestCallGmailFactory
"""


def main():
    # Build object with service-account
    mails_id = GmailDataFactory("dev").get_message_id(
        "me", include_spam_trash=True, max_results=10
    )
    for mail in mails_id:
        mails = GmailDataFactory("dev").get_message("me", mail["id"])
        print(mails)

    # call Methods to get all your mail

    # # Test 1
    # mail = GmailDataFactory(CLIENT_SECRET).get_message_by_thread('me')
    # with open('gmail_test.json', 'w') as outfile:
    #     json.dump(mail, outfile, indent=4)
    #
    # # Test 2
    # id = '16a4a42bc5d77074'
    # mail = GmailDataFactory(CLIENT_SECRET).get_message('me',id)
    # with open('gmail_test_2.json', 'w') as outfile:
    #     json.dump(mail, outfile, indent=4)

    # Rest 3
    # label_id = GmailDataFactory(CLIENT_SECRET).list_label('me')


if __name__ == "__main__":
    main()
