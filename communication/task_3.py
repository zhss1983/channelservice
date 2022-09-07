import argparse
import asyncio

from const import EVENING_SEND_TIME, MORNING_SEND_TIME, MY_ID, SECOND_UPDATE
from logger import logger
from sheduller import Sheduler
from task_1 import copy_sheet
from task_2 import db_update_from_googlesheets, session
from task_4 import check_overdue

morning_check = Sheduler(time=MORNING_SEND_TIME)
evening_check = Sheduler(time=EVENING_SEND_TIME)

my_id = MY_ID


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description="Отслеживание изменений в google таблице:")
    parser.add_argument("mode", choices=available_modes, help="Режимы работы:")
    parser.add_argument("-c", "--clear-cache", action="store_true", help="Очистка кеша")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Режим отладки")
    return parser


async def chek():
    while True:
        await morning_check(task=check_overdue)
        await evening_check(task=check_overdue)
        db_update_from_googlesheets(my_id)
        await asyncio.sleep(SECOND_UPDATE)


def run_check():
    logger.info(f"Запущен процесс отслеживания изменений в google таблице с id {my_id}")
    asyncio.run(chek())


def run_copy_sheet():
    global my_id
    logger.info(f"Запущен процесс копирования google таблицы.")
    my_id = copy_sheet()
    logger.info(f"Новый id {my_id}")


def main():
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
