from flask import Flask, render_template
import admin_bp
from database import Database, Aux
from core.wholesalers import wholesalers
from core.get_data import Getdata


# INIT APP
app = Flask(__name__)

# DATABASE
db = Database(app)
# CREATE TABLES
db.create_tables()

# DATA
data = Getdata(wholesalers, db)

# BLUEPRINTS
app.register_blueprint(admin_bp.construct_blueprint(data, db), url_prefix='/admin')


@app.route('/')
def index():
    print(app.url_map)
    return render_template('index.html')






if __name__ == "__main__":
    app.run(debug=True)