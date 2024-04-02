from flask import Blueprint, render_template, abort, redirect, url_for
from core.get_data import Getdata
from database import Database
import pandas
import time

def construct_blueprint(data: Getdata , db: Database):
    admin = Blueprint('admin', __name__, template_folder='templates')

    @admin.before_request
    def restrict_bp_to_admins():
        user = 'admin'
        if not  user == "admin":
            return redirect(url_for('index'))


    def update_products(list_data: pandas.DataFrame, list_prices, db_operator: Database):
        error_message = 'No connection with any  product supplier, product list was not updated please try again later.'
        errors = []
        if type(list_data) == pandas.DataFrame and type(list_prices) == pandas.DataFrame:
            db_operator.add_products(list_data)

            if data.supplier_errors:
                if len(data.supplier_errors) >= len(data.wholesalers):
                    return error_message
                else:
                    errors.append(data.supplier_errors)

            db_operator.add_product_prices(list_prices)
            if data.list_prices_errors:
                if len(data.list_prices_errors) >= len(data.wholesalers):
                    return error_message
                else:
                    errors.append(data.list_prices_errors)
            return errors
        else:
            return error_message


    @admin.route('/', methods=['GET'])
    def index():

        return render_template('/admin/home/index.html')

    @admin.route('update-products', methods=['GET'])
    def update():
        product_list = data.update_data()
        price_list = data.update_price_list(36.28)
        execute_update = update_products(product_list, price_list, db)
        return render_template('admin/update.html', errors=execute_update)


    return admin