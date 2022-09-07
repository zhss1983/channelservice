from pprint import pprint

from const import COPY_ID, CREDENTIALS_INFO, GOOGLE_DOC, SCOPES
from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from communication.google_api.drive import clear_disk, copy_obj, get_list_obj, set_user_permissions


def auth_drive():
    credentials = Credentials.from_service_account_info(info=CREDENTIALS_INFO, scopes=SCOPES)
    service = discovery.build("drive", "v3", credentials=credentials)
    return service, credentials


service, credentials = auth_drive()

list_obj = get_list_obj(service)
spreadsheets = list_obj["files"]
clear_disk(service, spreadsheets)

task_obj = copy_obj(service, COPY_ID)
set_user_permissions(task_obj["id"], credentials)
pprint(GOOGLE_DOC + task_obj["id"] + "/edit#gid=0")
