from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file, flash
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.supplier import Supplier
from database import Database
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit
from forms.forms import CheckOutCart



def construct_blueprint(db: Database, socketio: SocketIO, app):
    cart = Blueprint('cart', __name__, url_prefix='/cart')

    @socketio.on('connect')
    @login_required
    def handle_connect():
        print('client connected')


    @socketio.on('add_to_cart')
    @login_required
    def handle_add_to_cart(product_price_id, supplier_id, quantity):
        user = db.get_user(current_user.id)
        # check if product exist in the cart
        cart_item = db.check_product_cart(product_price_id, user.id)
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
            emit('update_quantity', {"quantity":new_item_quantity.quantity})


    @cart.route('/')
    @login_required
    def view_cart():
        form = CheckOutCart()
        user = db.get_user(current_user.id)
        shopping_cart = db.view_cart(user_id=user.id)
        return render_template('cart.html', shopping_cart=shopping_cart, form=form)

    @cart.route('/checkout', methods=['POST', 'GET'])
    @login_required
    def checkout_cart():
        if request.method == 'GET':
            return redirect(url_for('cart.view_cart'))

        if request.method == 'POST':
            supplier = request.form['supplier']
            user_id = current_user.id
            order = db.checkout_cart(user_id=user_id, supplier=supplier)
            for item in order:
                print(item)
        return "checking out cart"



    return cart

