from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload,MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class Upload:

    service = None

    def __init__(self):
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

        self.service = build('drive', 'v3', credentials=creds)

    def upload(self, name):
        file = self.uploadFile(name)
        print("Uploaded to Google Drive. File ID: " + file.get('id'))

        self.updatePermissions(file.get('id'))
        print("Updated permissions for anyone to see content.")

        link = self.getWebViewLink(file.get('id'))
        print("Obtained shareable link: " + link)

        return link, file.get('id')

    def uploadFile(self, name):
        # https://developers.google.com/drive/api/v3/manage-uploads#python
        file_metadata = {'name': name}
        media = MediaFileUpload(name, mimetype='video/mp4')
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        return file

    def updatePermissions(self, file_id):
        try:
            permission = {
                "role": "reader",
                "type": "anyone",
            }
            return self.service.permissions().create(fileId=file_id, body=permission).execute()
        except errors.HttpError as error:
            print('An error occurred:', error)
        return None

    def getWebViewLink(self, file_id):
        field = 'webViewLink'
        response = self.service.files().get(fileId=file_id, fields=field).execute()
        return response.get(field)

if __name__ == "__main__":
    print("Uploaded file to: " + Upload().upload("output.mp4")[0])