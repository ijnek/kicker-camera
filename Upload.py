from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload
from apiclient import errors

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


class Upload:

    _service = None

    def upload(self, name):
        file_name = self._uploadFile(name)
        self._updatePermissions(file_name)
        link = self._getWebViewLink(file_name)
        return link

    def __init__(self):
        credentials = None
        # The file token.json stores the user's access and refresh
        # tokens, and is created automatically when the authorization flow
        # completes for the first time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file(
                'token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and \
                    credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        self._service = build('drive', 'v3', credentials=credentials)

    def _uploadFile(self, name):
        # https://developers.google.com/drive/api/v3/manage-uploads#python

        print("INFO: Uploading " + name + " to Google Drive")
        file_metadata = {'name': name}
        media = MediaFileUpload(name, mimetype='video/mp4')
        file = self._service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        file_name = file.get('id')
        print("INFO: Successfully uploaded to Google Drive, file id is: " +
              file_name)
        return file_name

    def _updatePermissions(self, file_id):
        print("INFO: Updating google drive file permissions so anyone " +
              "can view the file")
        try:
            permission = {
                "role": "reader",
                "type": "anyone",
            }
            self._service.permissions() \
                .create(fileId=file_id, body=permission).execute()
            print("INFO: Successfully updated google drive file permissions")
        except errors.HttpError as error:
            print('ERROR: Failed updating google drive file permissions.\n'
                  + error)
            return False
        return True

    def _getWebViewLink(self, file_id):
        field = 'webViewLink'
        response = self._service.files().get(fileId=file_id, fields=field) \
            .execute()
        link = response.get(field)
        print("INFO: Obtained web view link: " + link)
        return link


if __name__ == "__main__":
    link = Upload().upload("output.mp4")
    print("Uploaded file to: " + link)
