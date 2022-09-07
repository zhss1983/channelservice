import asyncio

from const import DEBUG, MY_ID, SECOND_UPDATE
from task_1 import copy_sheet
from task_2 import db_update_from_googlesheets


async def run():
    if DEBUG:
        my_id = MY_ID
    else:
        my_id = copy_sheet()

    while True:
        db_update_from_googlesheets(my_id)
        await asyncio.sleep(SECOND_UPDATE)


if __name__ == "__main__":
    asyncio.run(run())
