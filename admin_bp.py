from flask import Blueprint, render_template, abort, redirect, url_for, request
from core.wholesalers import wholesalers
from core.update_data import UpdateData
from database import Database
from forms.forms import CsvForm, DeleteProduct, RegisterUserForm, RegisterPharmacyForm, EditUserForm
from werkzeug.security import generate_password_hash, check_password_hash

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
        last_products = db.last_products()
        return render_template('/admin/home/index.html', messages=message, last_products=last_products)

    @admin.route('/products', methods=['GET', 'POST'])
    def products():
        delete_product_form = DeleteProduct()

        messages = got_message()
        all_products = db.show_all_product(per_page=8)

        if delete_product_form.validate_on_submit():
            product_id = delete_product_form.product_id.data
            db.delete_product(product_id)
            return redirect(url_for('admin.products'))

        return render_template('admin/home/products.html', messages=messages, products=all_products,
                               form=delete_product_form)

    @admin.route('/users', methods=['GET', 'POST'])
    def users():
        ### forms ###
        form_user = RegisterUserForm()
        form_pharmacy = RegisterPharmacyForm()

        ### users ###
        registered_users = db.all_users()

        ### pharmacies ###
        registered_pharmacies = db.all_pharmacies()

        ### User form ###
        if form_user.submit_user.data and form_user.validate():
            email = form_user.email.data
            if db.check_user(email):
                print('This is email already taken.')
            else:
                new_user = db.add_user(
                    name=form_user.name.data,
                    last_name=form_user.last_name.data,
                    email=form_user.email.data,
                    password=generate_password_hash(form_user.password.data, method='pbkdf2:sha256', salt_length=8)
                )
                return redirect(url_for('admin.users', _anchor='users'))

        ### pharmacy form ###
        if form_pharmacy.submit_pharmacy.data and form_pharmacy.validate():
            user_email = form_pharmacy.user_email.data
            user_id = db.check_user(user_email)
            if user_id:
                new_pharmacy = db.add_pharmacy(
                    rif=form_pharmacy.rif.data,
                    name=form_pharmacy.name_pharmacy.data,
                    email=form_pharmacy.email_pharmacy.data,
                    address=form_pharmacy.address.data,
                    user_id=user_id.id
                )
                return redirect(url_for('admin.users', _anchor='pharmacies'))
            else:
                print('This user not exist in our records.')


        return render_template('admin/home/users.html', form_user=form_user,
                                                        form_pharmacy=form_pharmacy,
                                                        users=registered_users,
                                                        pharmacies=registered_pharmacies)

    @admin.route('/user-edit/<user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        user = db.get_user(user_id)
        form = EditUserForm(
            name=user.name,
            last_name=user.last_name,
            email=user.email,
        )
        if form.validate_on_submit():
            if form.password.data:
                print(form.password.data)
        return render_template('admin/home/user-edit.html', form=form, user=user)


    @admin.route('/suppliers', methods=['GET'])
    def suppliers():
        all_supplier = db.all_suppliers()
        return render_template('admin/home/suppliers.html', suppliers=all_supplier)

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
        new_data.errors = []
        return redirect(request.referrer)


    return admin