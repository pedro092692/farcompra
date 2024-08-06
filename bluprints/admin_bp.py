from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.file_manipulator.file_manipulator import FileHandler
from core.supplier import Supplier
from database import Database
from .user_bp import construct_blueprint as bp_user
from .supplier_bp import construct_blueprint as bp_supplier
from forms.forms import CsvForm, DeleteProduct, Dollar
from flask_login import login_user, current_user, login_required
import os
from flask_apscheduler import APScheduler

def construct_blueprint(db: Database, app):
    admin = Blueprint('admin', __name__, template_folder='templates')
    admin.register_blueprint(bp_user(db))
    new_data = UpdateData(wholesalers, db)
    admin.register_blueprint(bp_supplier(db, errors=new_data))
    # CRONJOB
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    update_rate = '30'

    def got_message():
        message = ''
        if new_data.errors:
            message = new_data.errors
        return message

    @admin.before_request
    def restrict_bp_to_admins():
        if not current_user.is_authenticated or current_user.role != 'admin':
            return abort(401)

    @admin.route('/', methods=['GET'])
    def index():
        message = got_message()
        last_products = db.last_products()
        last_users = db.last_users()
        return render_template('/admin/home/index.html', messages=message, last_products=last_products, last_users=last_users)

    @admin.route('/products', methods=['GET', 'POST'])
    def products():
        # deleting all garbage
        file_manipulator = FileHandler()
        file_manipulator.remove_all_files(path='core/data/manual_uploads')

        new_data.testing()
        delete_product_form = DeleteProduct()
        messages = got_message()
        all_products = db.show_all_product(per_page=8)

        if delete_product_form.validate_on_submit():
            product_id = delete_product_form.product_id.data
            db.delete_product(product_id)
            return redirect(url_for('admin.products'))

        return render_template('admin/home/products.html', messages=messages, products=all_products,
                               form=delete_product_form)

    @admin.route('/products/delete', methods=['GET', 'POST'])
    def delete_products():
        if request.method == 'POST':
            print('Time for reset all products....')
            db.delete_all_products()
            return redirect(url_for('admin.products'))

        return render_template('admin/home/delete_products.html')

    ### Delete shopping cart items ###
    @admin.route('/products/cart/delete', methods=['GET', 'POST'])
    def delete_shopping_cart():
        if request.method == 'POST':
            print('time for reset shopping cart....')
            db.delete_all_shopping_cart_items()
            return redirect(url_for('admin.index'))
        return render_template('admin/home/delete_shopping.html')

    ### Operations ###
    @admin.route('/update-now', methods=['GET'])
    def update_now():
        messages = got_message()
        new_data.download()
        return redirect(request.referrer)

    ### Cronjob ###
    @scheduler.task('cron', id='update_products', minute=f'*/{update_rate}', max_instances=5)
    def auto_update():
        with scheduler.app.app_context():
            # delete all notifications
            if new_data.errors:
                new_data.errors = []
            new_data.download()

    @admin.route('/uploads', methods=['POST'])
    def uploads():
        if request.method == 'POST':
            file = request.files.get('file')
            new_data.manually_upload(file)
        return 'file upload.'

    @admin.route('/delete-all-notifications', methods=['GET'])
    def delete_all_notifications():
        if new_data.errors:
            new_data.errors = []
        return redirect(request.referrer)

    @admin.route('/update-dollar', methods=['GET', 'POST'])
    def update_dollar():
        dollar_info = db.get_dollar_info()
        last_update = False

        form = Dollar()

        if form.validate_on_submit():
            dollar_value_form = form.value.data
            db.update_dollar_value(value=dollar_value_form)

            return redirect(url_for('admin.update_dollar'))

        if dollar_info:
            form.value.data = dollar_info.value
            last_update = dollar_info.date

        return render_template('admin/home/update-dollar.html', form=form, last_update=last_update)

    return admin
