from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload,MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
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
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)

def upload(name):
    file = uploadFile(name)
    updatePermissions(file.get('id'))
    link = getWebViewLink(file.get('id'))
    return link

def uploadFile(name):
    # https://developers.google.com/drive/api/v3/manage-uploads#python
    file_metadata = {'name': name}
    media = MediaFileUpload(name, mimetype='video/avi')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: ' + file.get('id'))
    return file

def updatePermissions(file_id):
    try:
        permission = {
            "role": "reader",
            "type": "anyone",
        }
        return service.permissions().create(fileId=file_id, body=permission).execute()
    except errors.HttpError as error:
        print('An error occurred:', error)
    return None

def getWebViewLink(file_id):
    field = 'webViewLink'
    response = service.files().get(fileId=file_id, fields=field).execute()
    return response.get(field)
