from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, IntegerField, RadioField, \
    SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from flask_babel import gettext, lazy_gettext


def string_field(label):
    return StringField(label=label, validators=[DataRequired()])

def email_field(label='Email'):
    return EmailField(label=label, validators=[DataRequired(), Email()])

def password_field():
    return PasswordField(label='Password', validators=[DataRequired()])

def submit_field(label, render_kw={}):
    return SubmitField(label=label, render_kw=render_kw)

### PRODUCTS ###
class CsvForm(FlaskForm):
    csv = FileField(gettext('Files'),
                    validators=[FileRequired(), FileAllowed(['csv', 'txt', 'xlsx', 'xls'],
          'Only Documents!')], render_kw={"class": "form-control", "multiple": True})
    submit = submit_field('Upload Files', render_kw={"class": "btn btn-primary"})


class DeleteProduct(FlaskForm):
    product_id = StringField(validators=[DataRequired()], render_kw={"class": "d-none"})
    submit = submit_field('Delete', render_kw={'class': 'btn btn-danger'})


### Users ###

class RegisterUserForm(FlaskForm):
    name = string_field(label='Name')
    last_name = string_field(label='Last Name')
    email = email_field()
    password = password_field()
    submit_user = submit_field(label='Register User')

class SearchUserForm(FlaskForm):
    query = email_field(label='User Email')
    submit_search = submit_field(label=lazy_gettext('Search User'))

class EditUserForm(FlaskForm):
    active = RadioField(label='User Is Active', default='Yes', choices=['yes', 'no'], validators=[DataRequired()])
    name = string_field(label='Name')
    last_name = string_field(label='Last Name')
    email = email_field()
    password = PasswordField(label='Password')
    role = RadioField(label='Type User', default='user', choices=['admin', 'user'], validators=[DataRequired()])
    submit_user = submit_field(label='Update User')


class QuickUser(FlaskForm):
    pharmacy_name = string_field(label='Pharmacy name')
    submit_user = submit_field(label='Add new user')

class DeleteUserForm(FlaskForm):
    user_id = StringField(validators=[DataRequired()], render_kw={"class": "d-none"})
    delete_user = submit_field('Delete', render_kw={'class': 'btn btn-danger'})

### Pharmacies ###


class RegisterPharmacyForm(FlaskForm):
    name_pharmacy = string_field(label='Pharmacy name')
    rif = IntegerField(label='RIF', validators=[DataRequired()])
    email_pharmacy = email_field()
    address = string_field(label='Address')
    user_email = email_field(label='User Email')
    submit_pharmacy = submit_field(label='Register Pharmacy')

class SearchPharmacyForm(FlaskForm):
    query_email = email_field(label='Pharmacy Email')
    submit_search_pharmacy = submit_field(label=lazy_gettext('Search Pharmacy'))


class PharmacyDiscount(FlaskForm):
    percent_discount = IntegerField(label='Percent Discount', validators=[DataRequired()])
    submit = submit_field('Save')


### Login ###

class LoginForm(FlaskForm):
    username = string_field(label='User Name')
    password = password_field()
    submit = submit_field(label=lazy_gettext('Sign in'))


### Suppliers ###
class SupplierForm(FlaskForm):
    name = string_field(label='Supplier name')
    submit = submit_field(label='save')



### Add To Cart ###

class AddToCart(FlaskForm):
    quantity = IntegerField(render_kw={'placeholder': gettext('Quantity')})
    submit = submit_field(gettext('Add To Cart'))

class CheckOutCart(FlaskForm):
    supplier = string_field(label='')
    submit = submit_field('Make order for')


### Dollar ###

class Dollar(FlaskForm):
    value = FloatField(label='Dollar Price', validators=[DataRequired()], render_kw={'placeholder': 'Dollar Value'})
    submit = submit_field('Update Dollar Price')





