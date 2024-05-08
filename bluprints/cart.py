from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file, flash, make_response
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.supplier import Supplier
from database import Database
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit
from forms.forms import CheckOutCart
from helpers import has_pharmacy
import pdfkit


def construct_blueprint(db: Database, socketio: SocketIO, app):
    cart = Blueprint('cart', __name__, url_prefix='/cart')

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    @socketio.on('connect')
    @login_required
    def handle_connect():
        print('client connected')

    @socketio.on('add_to_cart')
    @login_required
    @has_pharmacy
    def handle_add_to_cart(product_price_id, supplier_id, quantity):
        user = db.get_user(current_user.id)
        # check if product exist in the cart
        cart_item = db.check_product_cart(product_price_id, user.id)
        print(cart_item)
        if not cart_item:
            # Add product to the cart
            new_cart = db.add_to_cart(
                user_id=user.id,
                product_price_id=product_price_id,
                supplier_id=supplier_id,
                quantity=quantity
            )
        else:
            # Update only quantity
            new_item_quantity = db.update_cart(cart_item, quantity)
            emit('update_quantity', {"quantity": new_item_quantity.quantity})

    @socketio.on('update_cart_quantity')
    @login_required
    @has_pharmacy
    def handle_update_cart_quantity(item_id, quantity):
        cart_item = db.get_car_item(item_id)
        # update cart item quantity
        cart_item = db.update_cart_quantity(cart_item, quantity)
        total = cart_item.product_price_info.price * quantity
        grand_total = db.get_supplier_total(user_id=current_user.id, supplier_id=cart_item.supplier_id)
        emit('update_cart', {"total": round(total, 2),
                              "grand_total": grand_total,
                             "id": cart_item.id,
                             "supplier": cart_item.supplier_info.name,
                              })

    @socketio.on('delete_cart_item')
    @login_required
    @has_pharmacy
    def handle_delete_cart_item(cart_item_id):
        cart_item = db.get_car_item(cart_item_id)
        # Delete cart item
        db.delete_cart_item(cart_item=cart_item)

    @cart.route('/')
    @login_required
    @has_pharmacy
    def view_cart():
        form = CheckOutCart()
        user = db.get_user(current_user.id)
        shopping_cart = db.view_cart(user_id=user.id)
        return render_template('cart.html', shopping_cart=shopping_cart, form=form)


    @cart.route('/checkout', methods=['POST', 'GET'])
    @has_pharmacy
    @login_required
    def checkout_cart():
        if request.method == 'GET':
            return redirect(url_for('cart.view_cart'))

        if request.method == 'POST':
            supplier = request.form['supplier']
            user_id = current_user.id
            user = db.get_user(user_id)
            new_order = db.get_cart_by_supplier(user_id=user_id, supplier=supplier)

            rendered = render_template('order.html', order=new_order.all(), user=user, supplier=new_order[0].supplier_info.name)
            pdf = pdfkit.from_string(rendered, False, configuration=config,
                                     css='static/admin/assets/css/bootstrap/bootstrap.css')

            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename={new_order[0].supplier_info.name}_order.pdf'

            # Delete items from cart
            db.checkout_cart(user_id=user_id, supplier=supplier)

            return response

    return cart

