from sqlalchemy import select
from sqlalchemy.orm import Session

from order.models import Order


class OrderRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_by_id(self, user_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == user_id)
        return self.session.scalar(stmt)

    def create(self):
        pass

    def get_by_employee_id(self, employee_id: int) -> list[Order]:
        stmt = select(Order).where(Order.barista_id == employee_id)
        return self.session.scalars(stmt).unique().all()