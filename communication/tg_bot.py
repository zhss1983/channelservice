import telegram
from const import CHAT_ID, TELEGRAM_TOKEN
from logger import logger

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except telegram.error.NetworkError as error_network:
        logger.exception(
            f'Во время отправки возникла ошибка передачи данных ({error_network}). Cообщение "{message}" в чат не '
            "передано."
        )
    except telegram.error.TelegramError as error_telegram:
        logger.exception(
            f"При работе с telegram аккаунтом возникла ошибка {error_telegram}. Попытка отправить сообщение "
            f'"{message}" в чат провалилась.'
        )
    else:
        logger.info(f'Отправлено сообщение в чат, текст: "{message}"')
