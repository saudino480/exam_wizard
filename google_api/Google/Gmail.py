from __future__ import print_function
import pickle
import os
import base64
from googleapiclient.discovery import build
from apiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import mimetypes


class Gmail:
    def __init__(self, sender):
        self.send_address = sender
        self.service = self.setup_api()
        self.sender = sender

    def setup_api(self):
        # Setup the Google API
        SCOPES = ['https://mail.google.com/',
                  'https://www.googleapis.com/auth/gmail.send',
                  'https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token.pickle'):
            with open('./token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('./token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def create_message(self, to, subject, message_text):
        """
        Generate the email message (no attachment)
        :param to: string - recipients email address
        :param subject: string - email header
        :param message_text: string - email body
        :return: dictionary containing raw message
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def create_attached_message(self, to, subject, message_text, file_dir, filename):
        """
        Generate the email message (with attachement)
        :param to: string - recipients email address
        :param subject: string - email header
        :param message_text: string - email body
        :param file_dir: string - location of attachment file
        :param filename: string - name of file
        :return: dictionary containing raw message
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = self.sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        if main_type == 'text':
            fp = open(path, 'r')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            print(msg)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'r')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'r')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message(self, message):
        """
        Sends email to recepient
        :param message: dictionary containing raw message
        """
        try:
            message = (self.service.users().messages().send(userId='me', body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
