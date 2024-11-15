from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_user, logout_user, current_user

from auth.exceptions import UserDoesNotExistError
from auth.forms import LoginForm, RegisterForm
from auth.models import Employee
import auth.service as auth_srv

blueprint = Blueprint('auth', __name__)
prefix = '/auth'


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user: Employee = auth_srv.get_user_by_email(form.email.data)
            if user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('order.orders'))
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
        except UserDoesNotExistError:
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
    return render_template(prefix + '/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")
