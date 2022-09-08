import argparse
import asyncio

from const import EVENING_SEND_TIME, MORNING_SEND_TIME, MY_ID, SECOND_UPDATE
from logger import logger
from scheduler import Scheduler
from task_1 import copy_sheet
from task_2 import db_update_from_googlesheets, session
from task_4 import check_overdue

morning_check = Scheduler(time=MORNING_SEND_TIME)
evening_check = Scheduler(time=EVENING_SEND_TIME)

my_id = MY_ID


def configure_argument_parser(available_modes):
    """
    Конфигурирует модуль парсинга параметров вызова из командной строки.
    :param available_modes:
        Перечисление доступных режимов запуска.
    :return:
        Возвращает словарь аргументов с которыми была запущена программа.
        {
            'mode': str,  # Одно значение из списка available_modes
            'clear-cache': bool = False,
        }
    """
    parser = argparse.ArgumentParser(description="Отслеживание изменений в google таблице:")
    parser.add_argument("mode", choices=available_modes, help="Режимы работы:")
    parser.add_argument("-c", "--clear-cache", action="store_false", help="Очистка кеша")
    return parser


async def chek():
    """
    Запускает бесконечный цикл проверки изменений в google таблицах. Одновременно с этим запускает на выполнение
    проверку состояния всех объектов класса Scheduler (применяются для выполнения задач по расписанию).
    """
    while True:
        await morning_check(task=check_overdue)
        await evening_check(task=check_overdue)
        db_update_from_googlesheets(my_id)
        await asyncio.sleep(SECOND_UPDATE)


def run_check():
    """
    Выполняет запуск цикла асинхронной части приложения.
    """
    logger.info(f"Запущен процесс отслеживания изменений в google таблице с id {my_id}")
    asyncio.run(chek())


def run_copy_sheet():
    """Запускает копирование гугл документа"""
    global my_id
    logger.info(f"Запущен процесс копирования google таблицы.")
    my_id = copy_sheet()
    logger.info(f"Новый id {my_id}")


def main():
    """Запускается последовательно копирование документа и отслеживания изменения в нём."""
    try:
        run_copy_sheet()
        run_check()
    except KeyboardInterrupt:
        logger.info("Программа завершила свою работу, выполнение прервано пользователем.")
    exit(0)


MODE_TO_FUNCTION = {
    "copy": copy_sheet,
    "check": run_check,
    "full": main,
    "overdue": check_overdue,
}


if __name__ == "__main__":
    logger.info("Запущен программный комплекс для отслеживания и изменения заявок в БД.")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logger.info(f"Аргументы командной строки: {args}")
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode]()
