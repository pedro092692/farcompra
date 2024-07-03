from flask import Blueprint, render_template, render_template, url_for, redirect, flash, abort, session
from forms.forms import RegisterUserForm, RegisterPharmacyForm, EditUserForm, SearchUserForm, SearchPharmacyForm
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from flask_login import current_user

def construct_blueprint(db: Database):
    user = Blueprint('user', __name__, template_folder='templates')

    @user.route('/users', methods=['GET', 'POST'])
    def users():
        ### forms ###
        form_user = RegisterUserForm()
        form_pharmacy = RegisterPharmacyForm()
        form_search_user = SearchUserForm()
        form_search_pharmacy = SearchPharmacyForm()

        ### users ###
        registered_users = db.all_users()

        ### pharmacies ###
        registered_pharmacies = db.all_pharmacies()

        ### User form ###
        if form_user.submit_user.data and form_user.validate():
            email = form_user.email.data
            if db.check_user(email):
                form_user.email.errors.append('this email is already taken')
            else:
                new_user = db.add_user(
                    name=form_user.name.data,
                    last_name=form_user.last_name.data,
                    email=form_user.email.data,
                    password=generate_password_hash(form_user.password.data, method='pbkdf2:sha256', salt_length=8)
                )
                return redirect(url_for('admin.user.users', _anchor='users'))

        ### search user form ###

        if form_search_user.submit_search.data and form_search_user.validate():
            query = form_search_user.query.data.lower()
            searched_user = db.check_user(query)
            if searched_user and searched_user.id != current_user.id:
                return redirect(url_for('admin.user.edit_user', user_id=searched_user.id))
            else:
                form_search_user.query.errors.append('User not found')

        ### pharmacy form ###
        if form_pharmacy.submit_pharmacy.data and form_pharmacy.validate():
            user_email = form_pharmacy.user_email.data
            user_id = db.check_user(user_email)
            if user_id:
                if not user_id.pharmacy:
                    new_pharmacy = db.add_pharmacy(
                        rif=form_pharmacy.rif.data,
                        name=form_pharmacy.name_pharmacy.data,
                        email=form_pharmacy.email_pharmacy.data,
                        address=form_pharmacy.address.data,
                        user_id=user_id.id
                    )
                    return redirect(url_for('admin.user.users', _anchor='pharmacies'))
                else:
                    form_pharmacy.user_email.errors.append('This user already has a pharmacy.')
            else:
                form_pharmacy.user_email.errors.append('This user not exist in our records.')

        if form_search_pharmacy.submit_search_pharmacy.data and form_search_pharmacy.validate():
            query = form_search_pharmacy.query_email.data.lower()
            searched_pharmacy = db.check_pharmacy(email=query)
            if searched_pharmacy:
                return redirect(url_for('admin.user.pharmacy_edit', pharmacy_id=searched_pharmacy.id))
            else:
                form_search_pharmacy.query_email.errors.append('Pharmacy not found')

        return render_template('admin/home/users.html', form_user=form_user,
                               form_pharmacy=form_pharmacy,
                               users=registered_users,
                               pharmacies=registered_pharmacies,
                               form_search_user=form_search_user,
                               form_search_pharmacy=form_search_pharmacy)

    @user.route('/user-edit/<user_id>', methods=['GET', 'POST'])
    def edit_user(user_id):
        if current_user.id == int(user_id):
            return redirect(url_for('admin.user.users'))


        user_ob = db.get_user(user_id)
        form = EditUserForm(
            active=user_ob.active,
            name=user_ob.name,
            last_name=user_ob.last_name,
            email=user_ob.email,
            role=user_ob.role,

        )
        if form.validate_on_submit():
            password = user_ob.password

            if form.password.data:
                password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)

            db.edit_user(user_id=user_ob.id,
                         name=form.name.data,
                         last_name=form.last_name.data,
                         email=form.email.data,
                         password=password,
                         role=form.role.data,
                         active=form.active.data)


            flash('User Updated')
            return redirect(url_for('admin.user.users'))


        return render_template('admin/home/user-edit.html', form=form, user=user_ob)

    @user.route('/pharmacy-edit/<pharmacy_id>', methods=['GET', 'POST'])
    def pharmacy_edit(pharmacy_id):
        pharmacy = db.get_pharmacy(pharmacy_id)
        form = RegisterPharmacyForm(
            name_pharmacy=pharmacy.name,
            rif=pharmacy.rif,
            email_pharmacy=pharmacy.email,
            address=pharmacy.address,
            user_email=pharmacy.user_info.email
        )
        if form.validate_on_submit():
            user_exist = db.check_user(form.user_email.data)
            if user_exist:
                if user_exist.id == pharmacy.user_info.id or not user_exist.pharmacy:
                    db.edit_pharmacy(
                        pharmacy_id=pharmacy.id,
                        name=form.name_pharmacy.data,
                        rif=form.rif.data,
                        email=form.email_pharmacy.data,
                        address=form.address.data,
                        user_email=form.user_email.data,
                    )
                    flash('Pharmacy Updated')
                    return redirect(url_for('admin.user.users'))
                else:
                    form.user_email.errors.append('This user already has a pharmacy')
            else:
                form.user_email.errors.append('This user email do not exist in our database.')

        return render_template('admin/home/pharmacy-edit.html', form=form, pharmacy=pharmacy)


    return user

