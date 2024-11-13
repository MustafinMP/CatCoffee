from flask import abort, redirect, url_for
from flask_login import current_user


def only_for_barista(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.is_barista:
            print('called')
            return func(*args, **kwargs)
        return abort(403)
    return wrapper


def only_for_admin(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.is_admin:
            return func(*args, **kwargs)
        return abort(403)
    return wrapper