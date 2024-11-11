from typing import Callable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, declarative_base
from config import DB_NAME

SqlAlchemyBase = declarative_base()

__factory: Callable = None
DATABASE_URL = f"sqlite:///{DB_NAME}?check_same_thread=False"


def global_init() -> None:
    """Init a database session factory.

    :return: no return.
    """

    global __factory

    if __factory:
        return

    print(f"Подключение к базе данных {DB_NAME}")
    engine = sa.create_engine(DATABASE_URL, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from auth.models import User
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Return a new database session.

    :return: new database session object.
    """

    global __factory
    return __factory()

