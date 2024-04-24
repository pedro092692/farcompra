from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file, flash
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.supplier import Supplier
from database import Database
from flask_login import login_required, current_user


def construct_blueprint(db: Database):
    cart = Blueprint('cart', __name__, url_prefix='/cart')

    @cart.route('add_to_cart', methods=['POST'])
    @login_required
    def add_to_cart():
        user = db.get_user(current_user.id)
        # new_cart = db.add_to_cart(
        #     user_id=user.id,
        #     product_price_id=70,
        #     supplier_id=2,
        #     quantity=1
        # )
        return 'product added'


    @cart.route('/')
    @login_required
    def view_cart():
        user = db.get_user(current_user.id)
        shopping_cart = db.view_cart(user_id=user.id)
        # total_cart_amount = sum(item.product_info.price * item.quantity for item in shopping_cart)

        print(shopping_cart)
        return "cart view"



    return cart

