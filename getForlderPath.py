import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import sys


def authenticate():
    credentials = None
    workingDirectory = sys.path[0]
    tokenPath = f'{workingDirectory}/client_secret_682545918402-f4jk0qls9593q517prjasj1rf85l3841.apps.googleusercontent.com.json'
    if os.path.exists(tokenPath):
        credentials = Credentials.from_authorized_user_file(tokenPath)

    return credentials


def getFile(credentials):
    service = build('drive', 'v3', credentials=credentials)

    # 파라미터를 포함하여 files.list 메서드 호출
    results = service.files().list(
        corpora='user',
        includeItemsFromAllDrives=True,
        q="mimeType='application/vnd.google-apps.folder'",
        supportsAllDrives=True,
        supportsTeamDrives=True
    ).execute()

    # 결과 출력
    for file in results.get('files', []):
        print(f"Found folder: {file['name']} (ID: {file['id']})")


if __name__ == "__main__":
    credentials = authenticate()
    getFile(credentials)
