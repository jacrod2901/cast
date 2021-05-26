from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd


class EmailUtil:
    def __init__(self, email_config):  
        self.__email_config  = email_config     
        self.__email_from = self.__email_config['email_from']
        self.__email_subject = self.__email_config['email_subject']
        self.__email_content = self.__email_config['email_content']
        
    def __create_message(self, email_to):
        """Create a message for an email.
        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(self.__email_content)
        message['to'] = email_to
        message['from'] = self.__email_from
        message['subject'] = self.__email_subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    
    def __send_message(self, service, user_id, message):

        """Send an email message.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.
        Returns:
            Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)


    def __service_account_login(self):
        self.__credential_file_path = self.__email_config['credentials-path']
        self.__token_file_path = self.__email_config['token-path']


        # SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        # SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        SCOPES = ['https://mail.google.com/']

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.__token_file_path):
            creds = Credentials.from_authorized_user_file(self.__token_file_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__credential_file_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.__token_file_path, 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service

    def send_email(self, email_to):
        service = self.__service_account_login()
        # Call the Gmail API
        message = self.__create_message(email_to)
        sent = self.__send_message(service,'me', message)

