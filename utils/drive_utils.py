import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def gdrive_auth():
    """Autentikasi ke Google Drive."""
    gauth = GoogleAuth()

    if not os.path.exists("../config/client_secrets.json"):
        raise FileNotFoundError("File client_secrets.json tidak ditemukan.")

    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive



def upload_file_to_drive(drive, local_path, filename, folder_id=None):
    gfile = drive.CreateFile({
        'title': filename,
        'parents': [{'id': folder_id}] if folder_id else []
    })
    gfile.SetContentFile(local_path)
    gfile.Upload()

    file_id = gfile['id']
    file_link = f"https://drive.google.com/file/d/{file_id}/view"

    return file_link

# drive = gdrive_auth()
# local_path = 'output/output.pptx'  # Path file lokal kamu
# filename = 'output/output.pptx'          # Nama file di Google Drive
# folder_id = '1X2FUDVUN3s2wzVnj9w8daiDXMDYs7IDJ'
# aa=upload_file_to_drive(drive, local_path, filename, folder_id)
# print (aa)