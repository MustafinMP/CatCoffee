from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session

from order.models import Order, Position

statuses = {
    0: 'Создан',
    1: 'В работе',
    2: 'Готов к выдаче',
    3: 'выдан',
}


class OrderRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_by_id(self, user_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == user_id)
        return self.session.scalar(stmt)

    def create(self, barista_id: int, is_payment_method_cash: bool, status_id: int = 0):
        order = Order()
        order.barista_id = barista_id
        order.payment_method = 'Наличными' if is_payment_method_cash else 'По карте'
        order.status = statuses[status_id]
        self.session.add(order)
        self.session.commit()

    def get_by_employee_id(self, employee_id: int) -> list[Order]:
        stmt = select(Order).where(Order.barista_id == employee_id)
        return self.session.scalars(stmt).unique().all()

    def set_status(self, order_id, new_status_id: int):
        order = self.get_by_id(order_id)
        order.status = statuses[new_status_id]
        self.session.merge(order)
        self.session.commit()

    def add_position(self, order_id: int, product_id: int, count: int = 1):
        stmt = select(Position).where(
            and_(
                Position.order_id == order_id,
                Position.product_id == product_id
            )
        )
        position = self.session.scalar(stmt)
        if position is not None:
            position.count += count
            self.session.merge(position)
        else:
            position = Position()
            position.order_id = order_id
            position.product_id = product_id
            position.count = count
            self.session.add(position)
        self.session.commit()

    def remove_position(self, order_id: int, product_id: int, count: int = 1):
        stmt = select(Position).where(
            and_(
                Position.order_id == order_id,
                Position.product_id == product_id
            )
        )
        position = self.session.scalar(stmt)
        if position is not None:
            position.count -= count
            if position.count <= 0:
                self.session.delete(position)
            else:
                self.session.merge(position)
            self.session.commit()
