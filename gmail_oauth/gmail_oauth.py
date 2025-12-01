from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SECRET_PARENT_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL_SECRET_FILE_PATH= os.path.join(SECRET_PARENT_PATH,"credentials.json")
CLIENT_SECRET_FILE = FULL_SECRET_FILE_PATH
TOKEN_FILE = 'token.json'

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.labels',	
    'https://www.googleapis.com/auth/gmail.modify'
]

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    The user is asked to authorize access and credentials are saved to token.json.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 1. Refresh the Access Token silently
            creds.refresh(Request())
        else:
            # 2. Start the full OAuth flow (opens browser, listens on 127.0.0.1:8080)
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            # This line opens the browser and handles the redirect automatically
            creds = flow.run_local_server(port=0) 

        # 3. Save the credentials (including the Refresh Token) for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service object
    service = build('gmail', 'v1', credentials=creds)
    return service

