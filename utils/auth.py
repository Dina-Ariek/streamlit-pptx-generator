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
