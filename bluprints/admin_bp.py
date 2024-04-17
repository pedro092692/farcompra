from flask import Blueprint, render_template, abort, redirect, url_for, request, send_file
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.supplier import Supplier
from database import Database
from .user_bp import construct_blueprint as bp_user
from .supplier_bp import construct_blueprint as bp_supplier
from forms.forms import CsvForm, DeleteProduct

def construct_blueprint(db: Database):
    admin = Blueprint('admin', __name__, template_folder='templates')
    admin.register_blueprint(bp_user(db))
    new_data = UpdateData(wholesalers, db)
    admin.register_blueprint(bp_supplier(db, errors=new_data))

    def got_message():
        message = ''
        if new_data.errors:
            message = new_data.errors
        return message

    @admin.before_request
    def restrict_bp_to_admins():
        user = 'admin'
        if not  user == "admin":
            return redirect(url_for('index'))

    @admin.route('/', methods=['GET'])
    def index():
        message = got_message()
        last_products = db.last_products()
        return render_template('/admin/home/index.html', messages=message, last_products=last_products)

    @admin.route('/products', methods=['GET', 'POST'])
    def products():
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



    ### Operations ###
    @admin.route('/update-now', methods=['GET'])
    def update_now():
        messages = got_message()
        new_data.download()
        return redirect(request.referrer)

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


    return admin