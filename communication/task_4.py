import datetime

from const import OVERDUE_TIME
from db_access import Session
from models import Order
from tg_bot import send_message


def check_overdue():
    session = Session()

    overdue_time = datetime.date.today() - OVERDUE_TIME
    overdue_orders = (
        session.query(Order).filter(Order.is_active, Order.created_on <= overdue_time).order_by(Order.order)
    )

    message = [f"У вас имеется просроченные поставки:\n"]
    rub = usd = 0
    for order in overdue_orders:
        rub += order.rub_price
        usd += order.usd_price
        message.append(
            f'Поставка №{order.order}, дата создания {order.created_on.strftime("%d.%m.%Y")} на сумму '
            f"{order.usd_price:.2f}$ ({order.rub_price:.2f} руб).\n"
        )
        if len(message) > 25:
            send_message("\n".join(message))
            message = []
    message.append(f"Всего {overdue_orders.count()}, на общую сумму {usd:.2f}$ ({rub:.2f} руб).")
    send_message("\n".join(message))


if __name__ == "__main__":
    check_overdue()
