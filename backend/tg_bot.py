"""Реализует отправку сообщений в телеграм-бот."""
import telegram
from const import CHAT_ID, TELEGRAM_TOKEN
from logger import logger

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    """Отправляет текстовое сообщение message на телеграмм бот. Чат бота указан в CHAT_ID."""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except telegram.error.NetworkError as error_network:
        logger.exception(
            'Во время отправки возникла ошибка передачи данных (%s). Cообщение "%s" в чат не передано.',
            error_network,
            +message,
        )
    except telegram.error.TelegramError as error_telegram:
        logger.exception(
            "При работе с telegram аккаунтом возникла ошибка %s. Попытка отправить сообщение "
            '"%s" в чат провалилась.',
            error_telegram,
            message,
        )
    else:
        logger.info('Отправлено сообщение в чат, текст: "%s"', message)
