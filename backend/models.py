"""Формирует модель Order для работы с БД."""
from datetime import date

from db_access import engine
from sqlalchemy import Boolean, Column, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    """Модель для сохроанения заказов/заявок в БД."""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    usd_price = Column(Float, default=0.0, nullable=False)
    created_on = Column(Date, default=date.today, onupdate=date.today)
    rub_price = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Order {self.order}, created {self.created_on}>"

    def is_same(
        self,
        instance: dict["number":int, "order":int, "usd_price":float, "created_on":date],
    ) -> bool:
        """Проверяет все значения записи из БД на соответствие таковым в instance."""
        if len(instance) < 4:
            raise ValueError("Переданное табличное представление не соответствует требованиям.")
        return (
            self.number == instance.get("number", None)
            and self.order == instance.get("order", None)
            and self.usd_price == instance.get("usd_price", None)
            and self.created_on == instance.get("created_on", None)
        )


Base.metadata.create_all(engine)
