import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASEDIR = Path(__file__).resolve().parent.parent

GOOGLE_DOC = "https://docs.google.com/spreadsheets/d/"

COPY_ID = "1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g"

if os.path.exists("my_id.txt"):
    with open("my_id.txt", "r") as file:
        MY_ID = file.read()
else:
    MY_ID = "1Dzlpjq6p4x9a4EW8TDAu4M0Z2ge1AHI1CnXRmCLsleE"

DEBUG = False

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

VALUTE_URL = "http://www.cbr.ru/scripts/XML_daily.asp"
VALUTE_RCODE = "R01235"  # код валюты (см. https://www.cbr.ru/scripts/XML_valFull.asp)

SECOND_UPDATE = 15
