"""
COPY_ID - id документа который необходимо скопировать
POSTGRES_PASSWORD - пароль к базе данных (БД)
POSTGRES_HOST сервер на котором расположена БД
POSTGRES_USERNAME имя пользователя для подключения к БД
POSTGRES_PORT - порт подключения к БД
POSTGRES_DBNAME - имя БД
TELEGRAM_TOKEN - токен для взаимодействия с телеграмом
CHAT_ID - id чата в телеграмме для отправки сообщений
VALUTE_RCODE - код валюты (см. https://www.cbr.ru/scripts/XML_valFull.asp)
SECOND_UPDATE - время в секундах для обращения к gooogle серверу.
LOG_PATH - путь и имя файла для сохранения логов
DATE_FORMATS: tuple() - перечисление всех интерпретируемых форматов написания даты
OVERDUE_TIME: datetime.timedelta(days=90) - время через которое срок заявки/поставки считается просроченным.
MORNING_SEND_TIME/EVENING_SEND_TIME: datetime.time(hour=9, minute=0, second=0) - время на которое установлено оповещение
LOGER_FORMATTER - формат вывода логов
"""
import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASEDIR = Path(__file__).resolve().parent.parent

GOOGLE_DOC = "https://docs.google.com/spreadsheets/d/"

COPY_ID = "1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g"

if os.path.exists("my_id.txt"):
    with open("my_id.txt", "r", encoding="utf-8") as file:
        MY_ID = file.read()
else:
    MY_ID = "1fhWEawj7DtrfYaqKvxOqD_saP8Nwk38ql2-W3MDg0io"

DEBUG = False

POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_USERNAME = os.environ["POSTGRES_USERNAME"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DBNAME = os.environ["POSTGRES_DBNAME"]

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

VALUTE_URL = "http://www.cbr.ru/scripts/XML_daily.asp"
VALUTE_RCODE = "R01235"

SECOND_UPDATE = 15

LOG_PATH = BASEDIR / "logs"

DATE_FORMATS = (
    "%d.%m.%Y",
    "%d.%m.%y",
    "%d/%m/%Y",
    "%d/%m/%y",
    "%d-%m-%Y",
    "%d-%m-%y",
    "%d %b %Y",
    "%d %b %Y",
)

OVERDUE_TIME = datetime.timedelta(days=90)
MORNING_SEND_TIME = datetime.time(hour=9, minute=0, second=0)
EVENING_SEND_TIME = datetime.time(hour=17, minute=0, second=0)

LOGER_FORMATTER = "%(asctime)s %(levelname)s %(name)s:\t%(message)s"
