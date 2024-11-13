from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    barista_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    date: Mapped[date] = mapped_column(Date, default=date.today)
    status: Mapped[int] = mapped_column(String)
    payment_method: Mapped[str] = mapped_column(String)
    amount: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)


class Position(SqlAlchemyBase):
    __tablename__ = 'position'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    count: Mapped[int] = mapped_column(default=1)

    order = relationship('Order', foreign_keys=[order_id], backref='positions')
    product = relationship('Product', foreign_keys=[product_id])


class Product(SqlAlchemyBase):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    amount: Mapped[int] = mapped_column()