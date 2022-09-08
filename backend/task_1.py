from const import COPY_ID, GOOGLE_DOC
from google_api.drive import auth_drive, clear_disk, copy_obj, get_list_obj, set_user_permissions
from logger import logger


def clear(service):
    """
    Отчищает google диск от старых версий скопированных файлов.
    """
    list_obj = get_list_obj(service)
    spreadsheets = list_obj["files"]
    clear_disk(service, spreadsheets)


def copy_sheet():
    """Производит непосредственное копирование документа и предоставление прав доступа, возвращает новый id."""
    service, credentials = auth_drive()
    clear(service)  # Для решения нужно ли это делать необходима консультация.
    task_obj = copy_obj(service, COPY_ID)
    set_user_permissions(task_obj["id"], credentials)
    logger.info(f'Скопирована google таблица, адрес: {GOOGLE_DOC}{task_obj["id"]}/edit#gid=0')

    with open("my_id.txt", "w") as file:
        file.write(task_obj["id"])
        logger.info("id google таблицы сохранён на диск в файл ./my_id.txt")

    return task_obj["id"]


if __name__ == "__main__":
    copy_sheet()
