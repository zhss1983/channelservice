from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from communication.const import CREDENTIALS_FILE, CREDENTIALS_INFO, SCOPES

# credentials = Credentials.from_service_account_file(filename=CREDENTIALS_FILE, scopes=SCOPES)
credentials = Credentials.from_service_account_info(info=CREDENTIALS_INFO, scopes=SCOPES)
service_sheet = discovery.build("sheets", "v4", credentials=credentials)
service_drive = discovery.build("drive", "v3", credentials=credentials)
