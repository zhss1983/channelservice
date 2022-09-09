"""
SCOPES - Список необходимых для работы с Google Api прав.
CREDENTIALS_INFO - данные необходимые для входа на сервер
READ_GOOGLESHEET_RANGHE = "A1:Z1000" - Диапазон для чтения google таблиц
"""
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS_INFO = {
    "type": os.environ["TYPE"],
    "project_id": os.environ["PROJECT_ID"],
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"],
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": os.environ["AUTH_URI"],
    "token_uri": os.environ["TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"],
}

READ_GOOGLESHEET_RANGHE = "A1:Z1000"
