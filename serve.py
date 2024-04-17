from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from bluprints import admin_bp
from database import Database
from flask_dropzone import Dropzone
from flask_babel import Babel
from flask_wtf import CSRFProtect



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



# BLUEPRINTS
app.register_blueprint(admin_bp.construct_blueprint(db=db), url_prefix='/admin')


@app.route('/login')
def login():
    return render_template('admin/home/login.html')

@app.route('/')
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



if __name__ == "__main__":
    app.run(debug=True)