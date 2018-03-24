import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from .database import connect 

app = Flask(__name__)

#csrf
app.secret_key = 'bSecret'#app.config['SECRET_KEY']
csrf = CSRFProtect(app)
csrf.init_app(app)

#login manager
login_manager = LoginManager()
login_manager.init_app(app)

#database
db = os.path.dirname(os.path.abspath(__file__)) + "/products.db"
conn, cur = connect(db)

from . import views as views
app.register_blueprint(views.blueprint)







