from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient import discovery

BASEDIR = Path(__file__).resolve().parent

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
# https://www.googleapis.com/auth/drive.readonly

CREDENTIALS_FILE = BASEDIR / "keys" / "chennalservice-1db08e60e40a.json"
