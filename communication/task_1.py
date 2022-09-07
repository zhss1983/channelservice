from const import COPY_ID, GOOGLE_DOC
from google_api.drive import auth_drive, clear_disk, copy_obj, get_list_obj, set_user_permissions


def copy_sheet():
    service, credentials = auth_drive()

    list_obj = get_list_obj(service)
    spreadsheets = list_obj["files"]
    clear_disk(service, spreadsheets)

    task_obj = copy_obj(service, COPY_ID)
    set_user_permissions(task_obj["id"], credentials)
    print(GOOGLE_DOC + task_obj["id"] + "/edit#gid=0")

    with open("my_id.txt", "w") as file:
        file.write(task_obj["id"])
    return task_obj["id"]


if __name__ == "__main__":
    copy_sheet()
