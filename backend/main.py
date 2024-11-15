from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user

from auth.service import get_user_by_id
from auth.views import blueprint as blueprint_auth, prefix as prefix_auth
from order.views import blueprint as blueprint_order, prefix as prefix_order, blueprint_storage

from config import SECRET_KEY, HOST
import db_session

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = SECRET_KEY


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


app.register_blueprint(blueprint_auth, url_prefix=prefix_auth)
app.register_blueprint(blueprint_order, url_prefix=prefix_order)
app.register_blueprint(blueprint_storage, url_prefix='/storage')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('order.orders'))
    return redirect(url_for('auth.login'))


@app.errorhandler(404)
def error404(e):
    return render_template('errors/404.html')


def main():
    """Just a main function.

    :return: no return.
    """

    db_session.global_init()
    print('Запуск сервера')
    app.run(host=HOST)


if __name__ == '__main__':
    main()

