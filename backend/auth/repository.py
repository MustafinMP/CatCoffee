from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.exceptions import UserIsAlreadyExistsError
from auth.models import Employee


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_by_id(self, user_id: int) -> Employee | None:
        """Find user in database by id.

        :param user_id: the id of the user.
        :return: user object or none.
        """

        stmt = select(Employee).where(Employee.id == user_id)
        return self.session.scalar(stmt)

    def get_by_email(self, emlpoyee_email: str) -> Employee | None:
        """Find user in database by email.

        :param emlpoyee_email: the email of the user.
        :return: user object or none.
        """

        stmt = select(Employee).where(Employee.email == emlpoyee_email)
        return self.session.scalar(stmt)

    def add(self, name: str, email: str, password: str, is_barista: bool = True, is_admin: bool = False) -> Employee:
        if self.get_by_email(email) is not None:
            raise UserIsAlreadyExistsError

        employee = Employee()
        employee.full_name = name
        employee.email = email
        employee.set_password(password)
        employee.is_barista = is_barista
        employee.is_admin = is_admin
        self.session.add(employee)
        self.session.commit()
        return employee
