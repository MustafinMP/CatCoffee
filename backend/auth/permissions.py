from flask import abort
from flask_login import current_user


def only_for_barista(func):
    def wrapper(*args, **kwargs):
        if current_user.is_barista:
            return func(*args, **kwargs)
        return abort(403)


def only_for_admin(func):
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        return abort(403)
