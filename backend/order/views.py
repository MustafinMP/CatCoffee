from flask import Blueprint, render_template, redirect, url_for
import order.service as srv
from auth.permissions import only_for_barista
from order.forms import CreateOrderForm

blueprint = Blueprint('order', __name__)
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
    products = srv.get_all_products()
    return render_template(prefix + '/edit_order.html', products=products, order=order)


@only_for_barista
@blueprint.route('/add/<order_id>/<product_id>')
def add_position(order_id: int, product_id: int):
    srv.add_position_to_order(order_id, product_id)
    return redirect(f'/order/edit/{order_id}')