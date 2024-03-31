from flask import Blueprint, render_template, abort, redirect, url_for
from core.get_data import Getdata
from database import Database
import pandas

def construct_blueprint(data: Getdata , db: Database):
    admin = Blueprint('admin', __name__, template_folder='templates')

    @admin.before_request
    def restrict_bp_to_admins():
        user = 'admin'
        if not  user == "admin":
            return redirect(url_for('index'))

    @admin.route('/', methods=['GET'])
    def index():
        return render_template('admin/index.html')

    @admin.route('/update/products', methods=['GET'])
    def update_products():
        medicines = data.update_data()
        error_message = 'No connection with any  product supplier, product list was not updated please try again later.'

        if type(medicines) == pandas.DataFrame:
            db.add_products(medicines)
            if data.supplier_errors:
                errors = data.supplier_errors
                if len(errors) >= len(data.wholesalers):
                    errors = error_message
                else:
                    errors = data.supplier_errors
            else:
                errors = None
        else:
            errors = error_message
        return render_template('admin/update_products_list.html', errors=errors)


    @admin.route('/update/products-prices', methods=['GET'])
    def update_product_prices():
        error_message = 'Any list product file found please update list products First.'
        products_info = data.update_price_list(dollar_value=36.35)
        if type(products_info) == pandas.DataFrame:
            db.add_product_prices(products_info)
            if data.list_prices_errors:
                errors = data.list_prices_errors
                if len(errors) >= len(data.wholesalers):
                    errors = error_message
            else:
                errors = None
        else:
            errors = error_message

        return render_template('admin/update_products_prices.html', errors=errors)

    return admin