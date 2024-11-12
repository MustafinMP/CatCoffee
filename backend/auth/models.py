from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_session import SqlAlchemyBase
from sqlalchemy import String, TIMESTAMP, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    """Main user model.

    :param id: the unique user identification key.
    :param name: just the username.
    :param email: the email of the user.
    :param hashed_password: the hash of user password.
    :param created_date: the date, when user was benn created.
    """

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_barista: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    def set_password(self, password: str) -> None:
        """Create hash of user password and save it.

        :param password: no hashed password.
        :return: no return.
        """

        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check that the user password is valid.

        :param password: no hashed password.
        :return: result of checking.
        """

        return check_password_hash(self.hashed_password, password)
