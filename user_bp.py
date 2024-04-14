from flask import Blueprint, render_template, render_template, url_for, redirect
from forms.forms import RegisterUserForm, RegisterPharmacyForm, EditUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database

def construct_blueprint(db: Database):
    user = Blueprint('user', __name__, template_folder='templates')

    @user.route('/users', methods=['GET', 'POST'])
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
                return redirect(url_for('admin.user.users', _anchor='users'))

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
                return redirect(url_for('admin.user.users', _anchor='pharmacies'))
            else:
                print('This user not exist in our records.')

        return render_template('admin/home/users.html', form_user=form_user,
                               form_pharmacy=form_pharmacy,
                               users=registered_users,
                               pharmacies=registered_pharmacies)

    @user.route('/user-edit/<user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        user_ob = db.get_user(user_id)
        form = EditUserForm(
            name=user_ob.name,
            last_name=user_ob.last_name,
            email=user_ob.email,
        )
        if form.validate_on_submit():
            if form.password.data:
                print(form.password.data)
        return render_template('admin/home/user-edit.html', form=form, user=user_ob)

    return user

