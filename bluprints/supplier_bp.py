from flask import Blueprint, render_template, blueprints, url_for, redirect, send_file
from database import Database

def construct_blueprint(db: Database):
    supplier = Blueprint('supplier', __name__, template_folder='templates')


    @supplier.route('/suppliers', methods=['GET'])
    def suppliers():
        all_supplier = db.all_suppliers()
        return render_template('admin/home/suppliers.html', suppliers=all_supplier)

    return supplier