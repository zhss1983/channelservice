from google.oauth2.service_account import Credentials
from google_api.const import CREDENTIALS_INFO, SCOPES
from googleapiclient import discovery


def auth_drive():
    credentials = Credentials.from_service_account_info(info=CREDENTIALS_INFO, scopes=SCOPES)
    service = discovery.build("drive", "v3", credentials=credentials)
    return service, credentials


def get_list_obj(service):
    response = service.files().list()
    return response.execute()


def set_user_permissions(spreadsheet_id, credentials):
    permissions_body = {"type": "user", "role": "writer", "emailAddress": "zhss1983@gmail.com"}

    drive_service = discovery.build("drive", "v3", credentials=credentials)
    access_permission = drive_service.permissions().create(fileId=spreadsheet_id, body=permissions_body, fields="id")
    access_permission.execute()


def clear_disk(service, spreadsheets):
    for spreadsheet in spreadsheets:
        response = service.files().delete(fileId=spreadsheet["id"])
        response.execute()


def copy_obj(service, fileId):
    response = service.files().copy(fileId=fileId)
    return response.execute()
