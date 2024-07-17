import flask_excel
from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file, flash, make_response
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.supplier import Supplier
from database import Database
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit
from forms.forms import CheckOutCart
from helpers import has_pharmacy, discount_cart
import flask_excel as excel


def construct_blueprint(db: Database, socketio: SocketIO, app):
    cart = Blueprint('cart', __name__, url_prefix='/cart')

    # config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    @socketio.on('connect')
    @login_required
    def handle_connect():
        print('client connected')

    @socketio.on('add_to_cart')
    @login_required
    @has_pharmacy
    def handle_add_to_cart(product_price_id, supplier_id, quantity, sp_name, product_name, product_price, product_id):
        user = db.get_user(current_user.id)
        # check if product exist in the cart
        cart_item = db.check_product_cart(product_price_id, user.id)
        if not cart_item:
            # Add product to the cart
            new_cart = db.add_to_cart(
                user_id=user.id,
                product_price_id=product_price_id,
                quantity=quantity,
                supplier_id=supplier_id,
                supplier_name=sp_name,
                product_name=product_name,
                product_price=product_price,
                product_id=product_id,
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
        if not quantity:
            quantity = 1
        cart_item = db.update_cart_quantity(cart_item, quantity)
        total = cart_item.product_price * quantity
        grand_total = db.get_supplier_total(user_id=current_user.id, supplier_id=cart_item.supplier_id)

        if current_user.discount:
            user_discount = db.get_user_discounts(current_user.id)
            suppliers = [item for item in user_discount]
            if cart_item.supplier_id in suppliers:
                total = total * (1 - user_discount[cart_item.supplier_id]['discount'])
                grand_total = grand_total * (1 - user_discount[cart_item.supplier_id]['discount'])

        emit('update_cart', {"total": round(total, 2),
                              "grand_total": round(grand_total, 2),
                             "id": cart_item.id,
                             "supplier": cart_item.supplier_name,
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

        if current_user.discount:
            user_discount = db.get_user_discounts(current_user.id)
            discount_cart(shopping_cart=shopping_cart, user_discount=user_discount)

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

            db.delete_last_order_history(user_id=user_id, supplier_id=supplier)

            if new_order.all():
                # add record to order history:
                for item in new_order.all():
                    db.add_order_history(
                        user_id=user_id,
                        supplier_id=item.supplier_id,
                        product_name=item.product_name,
                        quantity=item.quantity,
                        price=item.product_price
                    )

                rendered = render_template('order.html', order=new_order.all(), user=user,
                                           supplier=new_order[0].supplier_name)
            else:
                return redirect(url_for('cart.view_cart'))


            # Delete items from cart
            db.checkout_cart(user_id=user_id, supplier=supplier)

            return rendered

    @cart.route('/order-history', methods=['GET', 'POST'])
    @has_pharmacy
    @login_required
    def order_history():
        form = CheckOutCart()
        user = db.get_user(current_user.id)
        user_history = db.view_history(user_id=user.id)
        return render_template('order-history.html', order_history=user_history, form=form)

    @cart.route('/checkout-history', methods=['POST', 'GET'])
    @has_pharmacy
    @login_required
    def checkout_history():
        if request.method == 'GET':
            return redirect(url_for('cart.view_cart'))

        if request.method == 'POST':
            supplier_id = request.form['supplier']
            order_history_supplier = db.get_history_by_supplier(user_id=current_user.id, supplier=supplier_id)
            user_pharmacy = current_user.pharmacy[0].name
            rif = current_user.pharmacy[0].rif

            rendered = render_template('order-history-rendered.html', order=order_history_supplier,
                                       pharmacy=user_pharmacy, rif=rif)

            return rendered

    @cart.route('/checkout-excel', methods=['POST', 'GET'])
    @has_pharmacy
    @login_required
    def download_file():
        order = db.get_cart_by_supplier(user_id=current_user.id, supplier=1).all()
        data = [
            ["Drogueria: Vital Clinic", "Cliente: Farmacia Luna", "RIF: j-12342343"],
            ["Producto", "Cantidad", "Precio", "Total"]
        ]

        for item in order:
            data.append([item.product_name, item.quantity, item.product_price,
                         round(item.product_price * item.quantity, 2)])

        return flask_excel.make_response_from_array(data, 'xlsx')


    return cart

