from flask import Blueprint, render_template, blueprints, url_for, redirect, send_file, current_app
from database import Database
from core.supplier import Supplier
def construct_blueprint(db: Database, errors):
    supplier = Blueprint('supplier', __name__, template_folder='templates')




    @supplier.route('/suppliers', methods=['GET'])
    def suppliers():
        load_suppliers = Supplier()
        list_suppliers = load_suppliers.supplier_list()
        ftp_suppliers = db.get_ftp_suppliers(list_suppliers['ftp'])
        no_ftp_suppliers = db.get_ftp_suppliers(list_suppliers['no_ftp'])
        return render_template('admin/home/suppliers.html', suppliers_ftp=ftp_suppliers,
                               no_ftp_suppliers=no_ftp_suppliers,
                               messages=errors.errors)

    @supplier.route('/suppliers/download/<supplier_id>')
    def download_from_supplier(supplier_id):
        supplier_ = db.get_supplier(supplier_id)
        new_supplier = Supplier(name=supplier_.name)
        file_data = new_supplier.download_file()
        if file_data:
            response = current_app.make_response(file_data)
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = f'attachment; filename={supplier_.name}.csv'
            return response
        else:
            errors.errors.append(new_supplier.errors)
            return redirect(url_for('admin.supplier.suppliers'))

    return supplier