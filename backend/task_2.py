"""Задание №2 - проверяет изменения в документе."""
import datetime
from http import HTTPStatus

import requests
import requests_cache
from bs4 import BeautifulSoup
from const import DATE_FORMATS, MY_ID, VALUTE_RCODE, VALUTE_URL
from db_access import Session
from google_api import service_sheet
from google_api.sheets import read_values
from logger import logger
from models import Order

cached_session = requests_cache.CachedSession(
    cache_name="valute_cache",
    backend="sqlite",
    filter_fn=lambda response: response.status_code == HTTPStatus.OK,
)


def get_course(
    date: datetime.date,
    session: requests.Session | requests_cache.CachedSession = cached_session,
):
    """
    Возвращает курс валют по курсу ЦБРФ на указанную дату
    date: дата на которую необходимо получить значение
    """
    response = session.get(VALUTE_URL, params={"date_req": date.strftime("%d/%m/%Y")})
    if response.status_code > HTTPStatus.BAD_REQUEST:
        logger.critical("Не удалось прочитать данные с сервера.")
        raise requests.RequestException
    soup = BeautifulSoup(response.text, features="lxml")
    valute = soup.find(name="valute", attrs={"id": VALUTE_RCODE})
    value = valute.find(name="value")
    return float(value.text.replace(",", "."))


def date_converter(date: str) -> datetime.date | None:
    """
    Пытается декодировать дату из различных возможных форматов. Форматы задаются через константы DATE_FORMATS
    :returns:
        datetime.date or None
    """
    for format_method in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(date, format_method).date()
        except ValueError:
            pass
    return None


def get_google_order_rep_to_dict(
    googlesheet_id,
) -> dict[int, int, float, datetime.date]:
    """
    Переводит полученные из документа с id=googlesheet_id данные в словарь.
    :returns:
           {
                'number': int,
                'order': int,
                'usd_price': float,
                'created_on': datetime.date,
            }
    """
    result = []
    for item in read_values(service_sheet, googlesheet_id)[1:]:
        if len(item) < 4:
            logger.warning(
                "Обнаружена запись с неполным заполнением, для обработки не хватает полей. Запись пропущена без "
                "сохранения в БД."
            )
            continue
        created_on = date_converter(item[3])
        if created_on is None:
            logger.warning(
                "Обнаружен неизвестный формат даты: %s. Запись пропущена без сохранения в БД.\n"
                "Обрабатываемые данные: %s",
                item[3],
                item,
            )
            continue
        result.append(
            {
                "number": int(item[0]),
                "order": int(item[1]),
                "usd_price": float(item[2]),
                "created_on": created_on,
            }
        )
    return result


# pylint: disable=R0912
def db_update_from_googlesheets(googlesheet_id: str):
    """
    Загружает данные из БД и из Google таблици и сравнивает их на предмет изменения. Все выявленные изменения
    актуализируются в соответствии с Google таблицей.
    """
    session = Session()

    active_orders = session.query(Order).filter(Order.is_active).order_by(Order.order)

    google_orders = sorted(
        get_google_order_rep_to_dict(googlesheet_id),
        key=lambda instance: instance["order"],
    )

    change_orders, position = [], 0

    for order in active_orders:
        if len(google_orders) <= position or order.order < google_orders[position]["order"]:
            # Есть в БД, но нет в гугл таблицах.
            order.is_active = False
            change_orders.append(order)
            continue
        while len(google_orders) > position and order.order > google_orders[position]["order"]:
            # Нет в БД, но появилось в гугл таблицах.
            cur_order = google_orders[position]
            cur_order["rub_price"] = get_course(date=cur_order["created_on"]) * cur_order["usd_price"]
            change_orders.append(Order(**cur_order))
            position += 1
        if len(google_orders) > position and order.order == google_orders[position]["order"]:
            # Есть и в БД и в Гугл таблицах, обновить или пропустить
            if order.is_same(google_orders[position]):
                position += 1
                continue
            for key in google_orders[position]:
                setattr(order, key, google_orders[position][key])
            change_orders.append(order)

    for position in range(position, len(google_orders)):
        course = get_course(date=google_orders[position]["created_on"])
        google_orders[position]["rub_price"] = course * google_orders[position]["usd_price"]
        change_orders.append(Order(**google_orders[position]))

    if change_orders:
        logger.info("Количество записей подвергающихся изменению: %s", len(change_orders))
    session.add_all(change_orders)
    session.commit()


if __name__ == "__main__":
    db_update_from_googlesheets(MY_ID)
