from const import COPY_ID, GOOGLE_DOC
from google_api.drive import auth_drive, clear_disk, copy_obj, get_list_obj, set_user_permissions
from logger import logger


def copy_sheet():
    service, credentials = auth_drive()

    list_obj = get_list_obj(service)
    spreadsheets = list_obj["files"]
    clear_disk(service, spreadsheets)

    task_obj = copy_obj(service, COPY_ID)
    set_user_permissions(task_obj["id"], credentials)
    logger.info(f'Скопирована googl таблица, адрес: {GOOGLE_DOC}{task_obj["id"]}/edit#gid=0')

    with open("my_id.txt", "w") as file:
        file.write(task_obj["id"])
        logger.info("id googl таблицы сохранён на диск в файл ./my_id.txt")

    return task_obj["id"]


if __name__ == "__main__":
    copy_sheet()
