from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.utils import secure_filename
from flask_babel import gettext


def submit_field(label, render_kw={}):
    return SubmitField(label=label, render_kw=render_kw)
class CsvForm(FlaskForm):
    csv = FileField(gettext('Files'),
                    validators=[FileRequired(), FileAllowed(['csv', 'txt', 'xlsx', 'xls'],
          'Only Documents!')], render_kw={"class": "form-control", "multiple": True})
    submit = submit_field('Upload Files', render_kw={"class": "btn btn-primary"})


class DeleteProduct(FlaskForm):
    product_id = StringField(validators=[DataRequired()], render_kw={"class": "d-none"})
    submit = submit_field('Delete', render_kw={'class': 'btn btn-danger'})
