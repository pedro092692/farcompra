from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from bluprints import admin_bp
from database import Database
from flask_dropzone import Dropzone
from flask_babel import Babel
from flask_wtf import CSRFProtect
from forms.forms import LoginForm
from werkzeug.security import check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from helpers import same_user



# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_here'
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
### DROPZONE ###
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.csv, .xlsx, .xls'
app.config['DROPZONE_MAX_FILE_SIZE'] = 10
app.config['DROPZONE_ENABLE_CSRF'] = True
csrf = CSRFProtect(app)

# DATABASE
db = Database(app)
# CREATE TABLES
db.create_tables()

# Plugins
Bootstrap5(app)
babel = Babel(app)
### Dropzone ###
dropzone = Dropzone(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)



# BLUEPRINTS
app.register_blueprint(admin_bp.construct_blueprint(db=db), url_prefix='/admin')


@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #check for if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # check if users exists
        user = db.check_user(username)
        if user:
            if check_password_hash(user.password, password):
                if user.active == 'yes':
                    login_user(user)
                    return redirect(url_for('index'))
                flash('Please Active your User')
            else:
                flash('Wrong user or password!')
        else:
            flash('Wrong user or password')
    return render_template('admin/home/login.html', form=form)

@app.route('/user/profile')
@login_required
def user_profile():
    user = db.get_user(current_user.id)
    return render_template('user_profile.html', user=user)

@app.route('/')
@login_required
def index():
    all_products = db.show_products()
    return render_template('index.html', products=all_products)

@app.route('/search')
def search():
    q = request.args.get('q')
    if q:
        results = db.search_products(q)
    else:
        results = db.show_products()

    return render_template('search_results.html', products=results)

@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    response = redirect(url_for('login'))
    response.cache_control.no_cache = True
    return response


# Errors
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)