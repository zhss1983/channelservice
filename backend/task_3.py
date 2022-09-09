"""
Задание №3, производит регулярную проверку документа. Дополнительно запускает по расписанию проверку просроченных
заявок/заказов. От сюда же реализован запуск первых двух заданий. Во время запуска воспользуйтесь ключом -h.
"""
import argparse
import asyncio
import sys

from const import EVENING_SEND_TIME, MORNING_SEND_TIME, MY_ID, SECOND_UPDATE
from logger import logger
from scheduler import Scheduler
from task_1 import copy_sheet
from task_2 import cached_session, db_update_from_googlesheets
from task_4 import check_overdue

morning_check = Scheduler(time=MORNING_SEND_TIME)
evening_check = Scheduler(time=EVENING_SEND_TIME)


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


async def chek(my_id: str = MY_ID):
    """
    Запускает бесконечный цикл проверки изменений в google таблицах. Одновременно с этим запускает на выполнение
    проверку состояния всех объектов класса Scheduler (применяются для выполнения задач по расписанию).
    """
    while True:
        await morning_check(task=check_overdue)
        await evening_check(task=check_overdue)
        db_update_from_googlesheets(my_id)
        await asyncio.sleep(SECOND_UPDATE)


def run_check(my_id: str = MY_ID):
    """
    Выполняет запуск цикла асинхронной части приложения.
    """
    logger.info("Запущен процесс отслеживания изменений в google таблице с id %s", my_id)
    asyncio.run(chek(my_id))


def run_copy_sheet() -> str:
    """Запускает копирование гугл документа, возвращает его id"""
    logger.info("Запущен процесс копирования google таблицы.")
    my_id = copy_sheet()
    logger.info("Новый id %s", my_id)
    return my_id


def main():
    """Запускается последовательно копирование документа и отслеживания изменения в нём."""
    try:
        my_id = run_copy_sheet()
        run_check(my_id)
    except KeyboardInterrupt:
        logger.info("Программа завершила свою работу, выполнение прервано пользователем.")
    sys.exit(0)


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
    logger.info("Аргументы командной строки: %s", args)
    if args.clear_cache:
        cached_session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode]()
