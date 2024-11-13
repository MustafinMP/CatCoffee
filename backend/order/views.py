from flask import Blueprint, render_template
import order.service as srv
from auth.permissions import only_for_barista

blueprint = Blueprint('order', __name__)
prefix = '/order'


@only_for_barista
@blueprint.route('/all')
def orders():
    orders = srv.get_all_orders()
    return render_template(prefix + '/orders.html', orders=orders)
