import os
from pathlib import Path

from dotenv import load_dotenv

BASEDIR = Path(__file__).resolve().parent.parent

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    # 'https://www.googleapis.com/auth/drive.readonly',
]

CREDENTIALS_FILE = BASEDIR / "keys" / "chennalservice-1db08e60e40a.json"

GOOGLE_DOC = "https://docs.google.com/spreadsheets/d/"

COPY_ID = "1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g"  # /edit#gid=0
MY_ID = "1Dzlpjq6p4x9a4EW8TDAu4M0Z2ge1AHI1CnXRmCLsleE"


SPREADSHEET_BODY = {
    "properties": {
        "title": "test",
        "locale": "ru_RU",
    },
    "sheets": [
        {
            "sheetType": "GRID",
            "title": "Лист1",
            "gridProperties": {
                "rowCount": 1000,
                "columnCount": 25,
            },
        }
    ],
}

load_dotenv()

EMAIL_USER = os.environ["EMAIL"]

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

DEBUG = False

POSTGRES_PASSWORD = "lehrjgjg"

VALUTE_URL = "http://www.cbr.ru/scripts/XML_daily.asp"
VALUTE_RCODE = "R01235"  # код валюты (см. https://www.cbr.ru/scripts/XML_valFull.asp)

READ_GOOGLESHEET_RANGHE = "A1:Z1000"
