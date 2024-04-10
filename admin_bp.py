import os
from flask import Blueprint, render_template, abort, redirect, url_for, request
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from database import Database
from forms.forms import CsvForm

def construct_blueprint(db: Database):
    admin = Blueprint('admin', __name__, template_folder='templates')
    new_data = UpdateData(wholesalers, db)

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
        return render_template('/admin/home/index.html', messages=message)

    @admin.route('/products', methods=['GET', 'POST'])
    def products():
        messages = got_message()
        return render_template('admin/home/products.html', messages=messages)

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
        new_data.errors = []
        return redirect(request.referrer)


    return admin