from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, IntegerField, RadioField, \
    SelectField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from flask_babel import gettext


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

class EditUserForm(FlaskForm):
    active = RadioField(label='User Is Active', default='Yes', choices=['yes', 'no'], validators=[DataRequired()])
    name = string_field(label='Name')
    last_name = string_field(label='Last Name')
    email = email_field()
    password = PasswordField(label='Password')
    role = RadioField(label='Type User',default='user', choices=['admin', 'user'], validators=[DataRequired()])
    submit_user = submit_field(label='Update User')

### Pharmacies ###

class RegisterPharmacyForm(FlaskForm):
    name_pharmacy = string_field(label='Pharmacy name')
    rif = IntegerField(label='RIF', validators=[DataRequired()])
    email_pharmacy = email_field()
    address = string_field(label='Address')
    user_email = email_field(label='User Email')
    submit_pharmacy = submit_field(label='Register Pharmacy')


### Login ###

class LoginForm(FlaskForm):
    username = string_field(label='User Name')
    password = password_field()
    submit = submit_field(label='Sign in')



### Add To Cart ###

class AddToCart(FlaskForm):
    quantity = IntegerField(render_kw={'placeholder': 'Quantity'})
    submit = submit_field('Add To Cart')

class CheckOutCart(FlaskForm):
    supplier = string_field(label='')
    submit = submit_field('Make order for')




