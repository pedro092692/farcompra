from flask import Blueprint, render_template, abort, redirect, url_for
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from database import Database

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

    @admin.route('/update-now', methods=['GET'])
    def update_now():
        new_data = UpdateData(wholesalers, db)
        if new_data.errors:
            print(new_data.errors)
        return redirect(url_for('admin.index'))



    return admin