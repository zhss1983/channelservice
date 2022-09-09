"""Рализует функции для работы с Google диском."""
from google.oauth2.service_account import Credentials
from google_api.const import CREDENTIALS_INFO, SCOPES
from googleapiclient import discovery


def auth_drive() -> (discovery.build, Credentials.from_service_account_info):
    """
    Генерирует и возвращает объекты необходимые для взаимодействия с Google Api (google диском).
    :return:
        service: объект для взаимиордействия с google диском.
        credentials: объект необходимый для получения прав и работы с сервисными службами google.
    """
    credentials = Credentials.from_service_account_info(info=CREDENTIALS_INFO, scopes=SCOPES)
    service = discovery.build("drive", "v3", credentials=credentials)
    return service, credentials


def get_list_obj(service: discovery.build) -> dict:
    """
    Возвращает список объектов (файлов) хранящихся на google диске.
    :param service:  объект необходимый для взаимиордействия с google диском.
    :return:
        Словарь формата:
        {
          'kind': 'drive#fileList',
          'nextPageToken': , str
          'incompleteSearch': bool
          'files': [
            {
              'id': str
              'kind': str  # тип объекта по отношению к гугл-диску: файл или папка.
              'mimeType': str.
              'name': str
            },
          ]
        }
    """
    response = service.files().list()
    return response.execute()


# pylint: disable=E1101
def set_user_permissions(spreadsheet_id, credentials, email):
    """
    Устанавливает разрешения на указанный объект google диска.
    :param spreadsheet_id: id объекта
    :param credentials: объект необходимый для получения прав и работы с сервисными службами google
    :return:
    """
    permissions_body = {"type": "user", "role": "writer", "emailAddress": email}
    drive_service = discovery.build("drive", "v3", credentials=credentials)
    access_permission = drive_service.permissions().create(fileId=spreadsheet_id, body=permissions_body, fields="id")
    access_permission.execute()


def clear_disk(service, spreadsheets):
    """Удаляет все файлы присланны в списке spreadsheets"""
    for spreadsheet in spreadsheets:
        response = service.files().delete(fileId=spreadsheet["id"])
        response.execute()


def copy_obj(service, file_id):
    """Копирует файл с Google диска, с id = file_id"""
    response = service.files().copy(fileId=file_id)
    return response.execute()
