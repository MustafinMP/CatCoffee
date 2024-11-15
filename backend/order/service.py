from flask_login import current_user

import db_session
from order.repository import OrderRepository, ProductRepository


def get_all_orders():
    with db_session.create_session() as session:
        repository = OrderRepository(session)
        return repository.get_by_employee_id(current_user.id)


def create_order(client_name):
    with db_session.create_session() as session:
        repository = OrderRepository(session)
        return repository.create(current_user.id, client_name)


def get_all_products():
    with db_session.create_session() as session:
        repository = ProductRepository(session)
        return repository.get_all()


def get_order(order_id):
    with db_session.create_session() as session:
        repository = OrderRepository(session)
        return repository.get_by_id(order_id)


def add_position_to_order(order_id, product_id):
    with db_session.create_session() as session:
        repository = OrderRepository(session)
        repository.add_position(order_id, product_id)
