
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


# Email variables. Modify this!
EMAIL_FROM = 'jacrod@orcasol.net'
EMAIL_TO = 'jaitssat@gmail.com'
EMAIL_SUBJECT = 'CAST NOTIFICATION'
EMAIL_CONTENT = 'THIS IS A NOTIFICATION ALERT FOR VACCINE AVAILABILITY'

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):

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

# def service_account_login():
#     SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#     SERVICE_ACCOUNT_FILE = '/home/jacrod2901/geese/cowin/test/service-key.json'

#     credentials = service_account.Credentials.from_service_account_file(
#           SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     delegated_credentials = credentials.with_subject(EMAIL_FROM)
#     service = build('gmail', 'v1', credentials=delegated_credentials)
#     return service
def service_account_login():
    # SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/jacrod2901/geese/cowin/test/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

service = service_account_login()
# Call the Gmail API
message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
sent = send_message(service,'me', message)
