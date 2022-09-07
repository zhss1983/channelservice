import asyncio
import datetime

from db_access import Session

session = Session()


class Sheduler:
    def __init__(self, time: datetime.time = datetime.time(hour=8), is_done=False):
        self.time = time
        self.is_done = is_done

    async def __call__(self, task=None, aiotask=None, *args, **kwargs):
        curent_time = datetime.datetime.now().time()
        hour = curent_time.hour - self.time.hour
        minute = curent_time.minute - self.time.minute + hour * 60
        seconds = curent_time.second - self.time.second + minute * 60
        if seconds > 60:
            await asyncio.sleep(60)
            return
        if seconds >= 0 and not self.is_done:
            await asyncio.sleep(seconds)
            if task is not None:
                task(*args, **kwargs)
            if aiotask is not None:
                await aiotask(*args, **kwargs)
        if seconds < 0 and self.is_done:
            self.is_done = False
