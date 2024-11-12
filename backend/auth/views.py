from flask import Blueprint, redirect, render_template
from flask_login import login_user, logout_user, current_user

from auth.exceptions import UserDoesNotExistError
from auth.forms import LoginForm, RegisterForm
from auth.models import User
import auth.service as auth_srv

blueprint = Blueprint('auth', __name__)
prefix = '/auth'


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                prefix + '/register.html',
                title='Регистрация',
                form=form,
                message="Пароли не совпадают"
            )
        if auth_srv.user_exists_by_email(form.email.data):
            return render_template(
                prefix + '/register.html',
                title='Регистрация',
                form=form,
                message="Такой пользователь уже есть"
            )
        auth_srv.add_user(form)
        return redirect(prefix + '/login')
    return render_template(prefix + '/register.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user: User = auth_srv.get_user_by_email(form.email.data)
            if user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect("/auth/profile")
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
        except UserDoesNotExistError:
            return render_template(prefix + '/login.html', message="Неправильный логин или пароль", form=form)
    return render_template(prefix + '/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")


@blueprint.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    return render_template(prefix + '/profile.html')
