from datetime import date, datetime

import requests_cache
from bs4 import BeautifulSoup

from communication import service_sheet
from communication.const import MY_ID, VALUTE_RCODE, VALUTE_URL
from communication.db_access import Session
from communication.google_api.sheets import read_values
from communication.models import Order


def get_course(date: date):
    """
    Возвращает курс валют по курсу ЦБРФ на указанную дату
    date: дата на которую необходимо получить значение
    """
    session = requests_cache.CachedSession(cache_name="valute_cache", backend="sqlite")
    response = session.get(VALUTE_URL, params={"date_req": date.strftime("%d/%m/%Y")})
    soup = BeautifulSoup(response.text, features="lxml")
    valute = soup.find(name="valute", attrs={"id": VALUTE_RCODE})
    value = valute.find(name="value")
    return float(value.text.replace(",", "."))


def get_google_order_rep(googlesheet_id):
    result = []
    for item in read_values(service_sheet, googlesheet_id)[1:]:
        if len(item) < 4:
            continue
        result.append(
            {
                "number": int(item[0]),
                "order": int(item[1]),
                "usd_price": float(item[2]),
                "created_on": datetime.strptime(item[3], "%d.%m.%Y").date(),
            }
        )
    return result


def db_update_from_googlesheets(googlesheet_id=MY_ID):
    session = Session()

    active_orders = session.query(Order).filter(Order.is_active).order_by(Order.order)

    google_orders = sorted(get_google_order_rep(googlesheet_id), key=lambda instance: instance["order"])

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
        if order.order == google_orders[position]["order"]:
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

    session.add_all(change_orders)
    session.commit()


if __name__ == "__main__":
    main()
