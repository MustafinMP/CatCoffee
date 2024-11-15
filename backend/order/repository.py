from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload

from order.models import Order, Position, Product

statuses = {
    0: 'Создан',
    1: 'В работе',
    2: 'Готов к выдаче',
    3: 'Выдан',
}


class OrderRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id).options(joinedload(Order.positions))
        return self.session.scalar(stmt)

    def create(self, barista_id: int, client_name: str, is_payment_method_cash: bool = True,
               status_id: int = 0):
        order = Order()
        order.barista_id = barista_id
        order.client_name = client_name
        order.payment_method = 'Наличными' if is_payment_method_cash else 'По карте'
        order.status = status_id
        self.session.add(order)
        self.session.commit()
        return order.id

    def get_by_employee_id(self, employee_id: int) -> list[Order]:
        stmt = select(Order).where(Order.barista_id == employee_id).options(joinedload(Order.positions))
        return self.session.scalars(stmt).unique().fetchall()

    def set_status(self, order_id, new_status_id: int):
        order = self.get_by_id(order_id)
        order.status = new_status_id
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

    def update_amount(self, order_id, amount):
        order = self.get_by_id(order_id)
        order.amount += amount
        self.session.merge(order)
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


class ProductRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_all(self) -> list[Product]:
        stmt = select(Product)
        return self.session.scalars(stmt).unique().all()

    def get_by_id(self, product_id):
        stmt = select(Product).where(Product.id == product_id)
        return self.session.scalar(stmt)
