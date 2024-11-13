from flask_login import current_user

import db_session
from order.repository import OrderRepository


def get_all_orders():
    with db_session.create_session() as session:
        repository = OrderRepository(session)
        return repository.get_by_employee_id(current_user.id)