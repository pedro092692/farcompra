from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap5
import admin_bp
from database import Database
from core.wholesalers import wholesalers
from flask_babel import Babel


# INIT APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_here'
app.config['BABEL_DEFAULT_LOCALE'] = 'es'

# DATABASE
db = Database(app)
# CREATE TABLES
db.create_tables()

# Plugins
Bootstrap5(app)
babel = Babel(app)


# BLUEPRINTS
app.register_blueprint(admin_bp.construct_blueprint(db=db), url_prefix='/admin')


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