import os
from flask import Blueprint, render_template, abort, redirect, url_for, request
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from database import Database
from forms.forms import CsvForm

def construct_blueprint(db: Database):
    admin = Blueprint('admin', __name__, template_folder='templates')

    @admin.before_request
    def restrict_bp_to_admins():
        user = 'admin'
        if not  user == "admin":
            return redirect(url_for('index'))

    @admin.route('/', methods=['GET'])
    def index():
        return render_template('/admin/home/index.html')

    @admin.route('/products', methods=['GET', 'POST'])
    def products():
        new_data = UpdateData(wholesalers, db)
        form = CsvForm()
        new_data.testing()
        return render_template('admin/home/products.html', form=form)

    @admin.route('/update-now', methods=['GET'])
    def update_now():
        new_data = UpdateData(wholesalers, db)
        new_data.download()
        if new_data.errors:
            print(new_data.errors)
        return redirect(request.referrer)

    @admin.route('/uploads', methods=['POST'])
    def uploads():
        new_data = UpdateData(wholesalers, db)
        if request.method == 'POST':
            file = request.files.get('file')
            new_data.manually_upload(file)
        return 'file upload.'


    return admin