"""Логирование событий через logger."""
import logging
from logging.handlers import TimedRotatingFileHandler

from const import LOG_PATH, LOGER_FORMATTER


def get_file_handler():
    """Запись логов в файл"""
    file_handler = TimedRotatingFileHandler(LOG_PATH, when="midnight", interval=1, encoding="utf-8", backupCount=14)
    formatter = logging.Formatter(LOGER_FORMATTER)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler():
    """Перенаправляет логи из sys.stderr"""
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(LOGER_FORMATTER)
    stream_handler.setFormatter(formatter)
    return stream_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(get_file_handler())
logger.addHandler(get_stream_handler())
