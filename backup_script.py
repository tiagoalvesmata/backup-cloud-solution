from __future__ import print_function
import os
import pickle
import io
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configurações
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'  # Substitua pelo caminho do arquivo de credenciais

def authenticate_google_drive():
    """Autentica e retorna um serviço do Google Drive"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def upload_file(service, file_path, folder_id=None):
    """Faz o upload de um arquivo para o Google Drive"""
    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    }
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path, mimetype=file_metadata['mimeType'])
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Arquivo "{file_path}" enviado com sucesso, ID: {file.get("id")}')

def list_files(service):
    """Lista arquivos no Google Drive"""
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('Nenhum arquivo encontrado.')
    else:
        print('Arquivos:')
        for item in items:
            print(f'{item["name"]} ({item["id"]})')

def main():
    service = authenticate_google_drive()
    
    # Exemplo de upload
    upload_file(service, 'path/to/your/file.txt')  # Substitua pelo caminho do arquivo que você deseja fazer o backup
    
    # Exemplo de listagem de arquivos
    list_files(service)

if __name__ == '__main__':
    main()

