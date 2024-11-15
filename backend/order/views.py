from flask import Blueprint, render_template, redirect, url_for
import order.service as srv
from auth.permissions import only_for_barista, only_for_admin
from order.forms import CreateOrderForm, AddToStorageForm
from order.repository import statuses

blueprint = Blueprint('order', __name__)
blueprint_storage = Blueprint('storage', __name__)
prefix = '/order'


@only_for_barista
@blueprint.route('/all')
def orders():
    orders = srv.get_all_orders()
    return render_template(prefix + '/orders.html', orders=orders)


@only_for_barista
@blueprint.route('/new', methods=['GET', 'POST'])
def new_order():
    form = CreateOrderForm()
    if form.validate_on_submit():
        order_id = srv.create_order(form.client_name.data)
        return redirect(f'edit/{order_id}')
    return render_template(prefix + '/new_order.html', form=form)


@only_for_barista
@blueprint.route('/edit/<order_id>', methods=['GET'])
def edit_order(order_id: int):
    order = srv.get_order(order_id)
    products = srv.get_exist_products()
    return render_template(prefix + '/edit_order.html', products=products, order=order, statuses=statuses)


@only_for_barista
@blueprint.route('/add/<order_id>/<product_id>')
def add_position(order_id: int, product_id: int):
    srv.add_position_to_order(order_id, product_id)
    return redirect(f'/order/edit/{order_id}')


@only_for_barista
@blueprint.route('/change-status/<order_id>/<status_id>')
def change_order_status(order_id: int, status_id: int):
    srv.change_order_status(order_id, int(status_id))
    return redirect(f'/order/edit/{order_id}')


@only_for_admin
@blueprint_storage.route('/')
def storage():
    products = srv.get_all_products()
    return render_template('/storage/storage.html', products=products)


@only_for_admin
@blueprint_storage.route('/add/<product_id>', methods=['GET', 'POST'])
def add(product_id):
    product = srv.get_product_by_id(product_id)
    form = AddToStorageForm()
    if form.validate_on_submit():
        srv.add_product_to_storage(product_id, form.count.data)
        return redirect(url_for('storage.storage'))
    return render_template('/storage/add.html', product=product, form=form)
