from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from flask_babel import gettext


def string_field(label):
    return StringField(label=label, validators=[DataRequired()])

def email_field():
    return StringField(label='Email', validators=[DataRequired()])

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
    submit = submit_field(label='Register User')


class RegisterPharmacyForm(FlaskForm):
    name = string_field(label='Pharmacy name')
    rif = IntegerField(label='RIF', validators=[DataRequired()])
    email = email_field()
    address = string_field(label='Address')
    submit = submit_field(label='Register Pharmacy')

