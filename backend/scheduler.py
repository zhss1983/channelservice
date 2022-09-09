"""Формирует обработчик события вызова функции запускаемой по расписанию"""
import asyncio
import datetime

from db_access import Session

session = Session()


# pylint: disable=R0903
class Scheduler:
    """Объект для установки таймера вызова функции. Требует запуска в бесконечном асинхронном цикле."""

    def __init__(self, time: datetime.time = datetime.time(hour=8), is_done=False):
        """
        Инициализация планировщика для выполнения задачь по расписанию.
        :parameter time:
            Время запуска, тип datetime.time. Врнмя можно установить вплоть до секунд, меньшие интервалы времени не
            учитываются.
        :parameter is_done:
            Выполнять или нет в первый раз в момент запуска после инициализации.
            False: не выполнялось ранее, надо запускать.
            True: ранее данное задание выполнялось, ждём следующих суток. Данный параметр не будет иметь значение если
            на текущие сутку по расписанию событию ещё только предстоит быть выполненным. То-еть установлено 17:00:00,
            а текущее время 10:28:32. Событие всё равно выполнится в 17:00:00.
        """
        self.__time = time
        self.__is_done = is_done

    async def __call__(self, *args, task=None, **kwargs):
        """
        Выполняет проверку не наступило ли ещё указанное время, если наступило - выполняет задачу task.
        *args и **kwargs будут переданны в задачи.
        """
        curent_time = datetime.datetime.now().time()
        hour = curent_time.hour - self.__time.hour
        minute = curent_time.minute - self.__time.minute + hour * 60
        seconds = curent_time.second - self.__time.second + minute * 60
        if seconds > 60:
            await asyncio.sleep(60)
            return
        if seconds >= 0 and not self.__is_done:
            await asyncio.sleep(seconds)
            if task is not None:
                task(*args, **kwargs)
        if seconds < 0 and self.__is_done:
            self.__is_done = False
