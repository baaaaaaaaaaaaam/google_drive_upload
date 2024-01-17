import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import sys


# 스크립트 실행 중인 디렉토리의 절대 경로 가져오기
workingDirectory = sys.path[0]

def authenticate():
    tokenPath = f'{workingDirectory}/client_secret_682545918402-f4jk0qls9593q517prjasj1rf85l3841.apps.googleusercontent.com.json'
    credentials = None
    if os.path.exists(tokenPath):
        credentials = Credentials.from_authorized_user_file(tokenPath)
    
    return credentials

def upload_to_drive(credentials):
    drive_service = build('drive', 'v3', credentials=credentials)
    targetFolderId = '11rKlOSsJltv06q3lhVojQ9Klq5ffobWI'
    fileName= 'djwkak.png'
    originFilePath = f'{workingDirectory}/{fileName}'
    targetFileName = fileName

    # 파일 업로드
    file_metadata = {'name': targetFileName}
    if targetFolderId:
        file_metadata['parents'] = [targetFolderId]


    media = MediaFileUpload(originFilePath, resumable=True)
    file = drive_service.files().create(
        body=file_metadata, 
        media_body=media,
        supportsAllDrives=True,
        supportsTeamDrives=True
        ).execute()

    print(f'File ID: {file["id"]}')
    print(f'File uploaded successfully to Google Drive.')

if __name__ == "__main__":
    credentials = authenticate()
    upload_to_drive(credentials)
