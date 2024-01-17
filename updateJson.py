from google_auth_oauthlib.flow import InstalledAppFlow
import sys


def authenticate():
    current_working_directory = sys.path[0]
    token_path = f'{current_working_directory}/client_secret_682545918402-f4jk0qls9593q517prjasj1rf85l3841.apps.googleusercontent.com.json'
    scopes = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file']
    flow = InstalledAppFlow.from_client_secrets_file(token_path, scopes)
    credentials = flow.run_local_server(port=0)
    # 토큰 저장
    with open(token_path, 'w') as token_file:
        token_file.write(credentials.to_json())


if __name__ == "__main__":
    authenticate()
