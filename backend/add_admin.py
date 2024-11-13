import db_session
from auth.repository import EmployeeRepository

name = input('Name: ')
email = input('Email: ')
password = input('Password: ')
is_barista = input('Is barista? ').lower() == 'y'
is_admin = input('Is admin? ').lower() == 'y'
db_session.global_init()
with db_session.create_session() as session:
    repository = EmployeeRepository(session)
    repository.add(name, email, password, is_barista, is_admin)