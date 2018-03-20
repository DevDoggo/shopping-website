import os

from flask import Flask #, render_template, request
from flask_wtf import CSRFProtect

from .database import connect 
#from .forms import ProductForm

app = Flask(__name__)

#csrf
app.secret_key = 'boye234234234234sdfsd_asdfadsf'#app.config['SECRET_KEY']
csrf = CSRFProtect(app)

#database
db = os.path.dirname(os.path.abspath(__file__)) + "/products.db"
conn, cur = connect(db)

from . import views as views
app.register_blueprint(views.blueprint)







