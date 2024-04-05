from flask import Blueprint, render_template, abort, redirect, url_for
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from core.file_manipulator.file_manipulator import FileHandler

def construct_blueprint():
    admin = Blueprint('admin', __name__, template_folder='templates')

    @admin.before_request
    def restrict_bp_to_admins():
        user = 'admin'
        if not  user == "admin":
            return redirect(url_for('index'))

    @admin.route('/', methods=['GET'])
    def index():
        new_data = UpdateData(wholesalers)
        if new_data.errors:
            print(new_data.errors)
        file_handler = FileHandler()
        file_handler.data_frame_products()
        return render_template('/admin/home/index.html')



    return admin