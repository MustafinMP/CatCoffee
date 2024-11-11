import db_session
from auth.exceptions import UserDoesNotExistError
from auth.forms import RegisterForm
from auth.models import User
from auth.repository import UserRepository


def get_user_by_id(user_id: int) -> User | None:
    """Find user in database by id.

    :param user_id: the id of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        repository = UserRepository(session)
        return repository.get_by_id(user_id)


def get_user_by_email(user_email: str) -> User | None:
    """Find user in database by email.

    :param user_email: the email of the user.
    :return: user object or none.
    """

    with db_session.create_session() as session:
        repository = UserRepository(session)
        user = repository.get_by_email(user_email)
        if not user:
            raise UserDoesNotExistError
        return user


def user_exists_by_email(user_email: str) -> bool:
    """Check that user exists in database.

    :param user_email: the email of the user.
    :return: user object or none.
    """
    try:
        get_user_by_email(user_email)
        return True
    except UserDoesNotExistError:
        return False


def add_user(form: RegisterForm) -> None:
    """Create new user by data from register form.

    :param form: the valid form with register data.
    :return: no return.
    """

    with db_session.create_session() as session:
        user_repository = UserRepository(session)
        user = user_repository.add(
            form.name.data,
            form.surname.data,
            form.email.data,
            form.password.data
        )
