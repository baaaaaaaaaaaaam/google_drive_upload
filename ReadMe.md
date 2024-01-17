### 파이썬으로 만든 결과물을 구글 드라이브의 원하는 폴더에 업로드 하는 방법

> 사전 준비
> 

---

1. 구글 계정
2. 파이썬 3.8.10
3. vscode 
4. ChatGPT ( 없어두됨 ㅎㅎ )

> 절차
> 

---

1. google cloud project 생성
2. OAuth 생성
3. 인증
4. python 으로 구글 드라이브  folder Id 가져오기
5. upload

> 따라하기
> 

---

- google cloud project 생성
    1. google cloud console 접속 후 프로젝트 생성
    2. 원하는 이름으로 프로젝트 생성
    3. “빠른 엑세스 > API 및 서비스” 선택
    4. 왼쪽 탭의 “라이브러리” 선택
    5. “Google Workspace” 카테고리 중 “Google Drive API “ 선택
    6. “Google Drive API “의  사용 선택
    
        ![1](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/c4a35971-4855-48ad-91a6-f69e061fd3e2)
    7. “사용자 인증 정보 만들기” 선택
        ![2](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/69cacd19-6832-457a-ae99-17a060ee11f6)
        
- OAuth 생성
    1. “사용자 데이터” 선택
    2. 앱 이름, 사용자 지원 이메일, 개발자 연락처 정보 입력
    3. 범위는 PASS
    4. “OAuth 클라이언트 유형” 을 드롭다운하여 맞는 형태로 사용 ( 저는 파이썬으로 연동할꺼라서 ‘데스크톱 앱’을 선택햇는데 되긴하더라고요 )
    5. “내 사용자 인증 정보” 에서 json 파일 다운로드
- 인증
    1. 다운 받은 json을 실행 프로젝트 폴더로 이동
    2. > pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    3. 아래 코드 실행
        
        ```python
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
        ```
        
    4. “Google Drive 파일 보기,생성,수정,삭제 권한” 과 “ 특정 Google Drive 한해 확인,수정, 생성, 삭제 권한” 허용
        
        ![3](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/65471691-e68c-41d3-965a-e30e28ca3365)

        
    5. 다운 받은 Json 파일의 내용 확인
        
        ![4](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/30369c94-b257-4160-8d19-7bcface6334d)
        권한 허용 전
        
        ![5](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/9e0efee4-ca5a-46f1-ade9-4ce59d2da1e4)
        권한 허용 후
        
- 구글 드라이브 폴더-ID 가져오기
    1. 아래 코드 실행
        
        ```python
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
        ```
        
    2. 결과 확인
        
        ![6](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/c61eb79f-69f8-4b9a-a86d-65c1564fc345)

        
    3. 원하는 폴더-ID 복사 
- 원하는 폴더에 파일  Upload
    1. 아래 코드 실행
    
    ```python
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
        targetFolderId = 'copy-folder-id'
        fileName= 'origin-file-name'
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
    ```
    
    2.  결과 확인
        
        ![7](https://github.com/baaaaaaaaaaaaam/google_drive_upload/assets/57000871/075965ce-8076-4ee0-9ea7-49758f9f3fc8)

        

> 참고문헌
> 

---

[Method: files.list  |  Google Drive  |  Google for Developers](https://developers.google.com/drive/api/reference/rest/v3/files/list?hl=ko)

[Method: files.create  |  Google Drive  |  Google for Developers](https://developers.google.com/drive/api/reference/rest/v3/files/create?hl=ko)