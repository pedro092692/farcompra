from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_bootstrap import Bootstrap5
from bluprints import admin_bp, cart
from database import Database
from flask_dropzone import Dropzone
from flask_babel import Babel, gettext
from flask_wtf import CSRFProtect
from forms.forms import LoginForm, AddToCart, PharmacyDiscount, RegisterUserForm
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from helpers import calc_discount, is_active
from dotenv import load_dotenv
from datetime import datetime
from flask_migrate import Migrate
import flask_sockets
import flask_excel as excel
import os


# Load env
load_dotenv()

# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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
# MIGRATIONS
migrate = Migrate(app, db.db)

# Plugins
Bootstrap5(app)
babel = Babel(app)
# excel
excel.init_excel(app)

### Dropzone ###
dropzone = Dropzone(app)

# websockets IO
# socketio = SocketIO(app, async_mode='eventlet')
socketio = SocketIO()
socketio.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

# BLUEPRINTS
app.register_blueprint(admin_bp.construct_blueprint(db=db, app=app), url_prefix='/admin')
app.register_blueprint(cart.construct_blueprint(db=db, socketio=socketio, app=app))


@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id=user_id)


@app.route('/register', methods=['GET', 'POST'])
def first_register():
    all_user = db.all_users()
    if not all_user:
        form = RegisterUserForm()
        if form.validate_on_submit():
            new_user = db.add_user(
                name=form.name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8),
                role='admin'
            )
            return redirect(url_for('login'))

        return render_template('register.html', form=form)
    else:
        return abort(404)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check for if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # check if users exists
        user = db.check_user(username.lower())
        if user:
            if check_password_hash(user.password, password):
                if user.active == 'yes':
                    login_user(user)
                    return redirect(url_for('index'))
                flash(gettext('Please Active your User'))
            else:
                flash(gettext('Wrong user or password!'))
        else:
            flash(gettext('Wrong user or password'))
    return render_template('admin/home/login.html', form=form)


@app.route('/user/profile', methods=['GET'])
@login_required
@is_active
def user_profile():
    user = db.get_user(current_user.id)
    suppliers = db.all_suppliers()
    discount = {}
    if current_user.discount:
        for user_discount in current_user.discount:
            discount[user_discount.supplier_id] = {
                "discount_supplier": user_discount.discount
            }
    return render_template('user_profile.html', user=user, suppliers=suppliers, user_discount=discount)


@app.route('/')
@login_required
@is_active
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
@login_required
@is_active
def search():
    form = AddToCart()
    prices_discount = []
    discount_suggest = []
    if request.args.get('barcode'):
        barcode = request.args.get('barcode')
        results = db.search_products(barcode, per_page=15)
        suggest = request.args.get('query')

        if current_user.discount:
            user_discount = db.get_user_discounts(current_user.id)
            suppliers = [item for item in user_discount]
            prices_discount = calc_discount(results, suppliers, user_discount)

    elif request.args.get('query'):
        results = db.search_products(request.args.get('query'), per_page=15)
        barcode = request.args.get('query')
        suggest = request.args.get('query')
        suggested_results = []

        if current_user.discount:
            user_discount = db.get_user_discounts(current_user.id)
            suppliers = [item for item in user_discount]
            prices_discount = calc_discount(results, suppliers, user_discount)
            discount_suggest = []

    else:
        return redirect(url_for('index'))

    if request.args.get('barcode'):
        if request.args.get('barcode') != request.args.get('query'):
            suggested_results = db.search_products(suggest, per_page=15)

            if current_user.discount:
                user_discount = db.get_user_discounts(current_user.id)
                suppliers = [item for item in user_discount]
                discount_suggest = calc_discount(suggested_results, suppliers, user_discount)
        else:
            suggested_results = []
            discount_suggest = []

    return render_template('search.html', results=results, search_query=barcode, suggested_results=suggested_results,
                           suggest=suggest, form=form, prices_discount=prices_discount,
                           discount_suggest=discount_suggest, get_text=gettext)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    response = redirect(url_for('login'))
    response.cache_control.no_cache = True
    return response


@socketio.on('connect')
def handle_connect():
    print('client connected!')


@socketio.on('search_query')
def handle_search_query(search_query, per_page):
    if search_query:
        results = db.search_products(q=search_query, per_page=per_page)
        emit('search_results', {'results': [item.serialize() for item in results if item.prices],
                                'pages': [page for page in results.iter_pages()],
                                'page': results.page,
                                'total': results.total,
                                'has_prev': results.has_prev,
                                'has_next': results.has_next,
                                'search_query': search_query,
                                })
    else:
        emit('search_results', {'results': []})


@socketio.on('update_discount')
def handle_search_query_discount(supplier_id, discount_amount):
    discount_amount = float(discount_amount) / 100

    # check if exist discount
    discount_user = db.get_user_discount(current_user.id, supplier_id)
    if discount_user:
        if discount_amount == 0:
            db.delete_user_discount(user_discount=discount_user[0])
        else:
            db.edit_user_discount(discount_user[0], discount_amount)
    else:
        # Add discount
        new_discount = db.add_discount(current_user.id, supplier_id, discount_amount)


# Cart
@app.context_processor
def get_cart():
    if current_user.is_authenticated:
        shopping_cart = db.view_cart(user_id=current_user.id)
        return {"shopping_cart": shopping_cart}
    else:
        return {"shopping_cart": {}}

# Date
@app.context_processor
def date():
    current_year = datetime.now().year
    return {'current_year': current_year}


# Errors
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.errorhandler(401)
def custom_401(error):
    return render_template('admin/home/page-404.html')

@app.errorhandler(404)
def custom_404(error):
    return render_template('admin/home/page-404.html')


if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=False)



