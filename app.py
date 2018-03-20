import os

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from .database import connect, add_product, show 
from .forms import ProductForm

app = Flask(__name__)

#csrf
app.secret_key = 'boye234234234234sdfsd_asdfadsf'#app.config['SECRET_KEY']
csrf = CSRFProtect(app)

#database
db = os.path.dirname(os.path.abspath(__file__)) + "/products.db"
conn, cur = connect(db)





@app.route('/')
def Default():
    db.show()
    return render_template("default.html")


@app.route('/products', methods=['GET', 'POST'])
@app.route('/products/<prod_id>', methods=['GET', 'POST'])
def Products(prod_id=None):
    if (prod_id == None):
        return render_template("products.html")
    else:
        return render_template("products.html", prod_id=prod_id) 


@app.route('/add', methods=['GET', 'POST'])
@app.route('/add/<name>', methods=['GET', 'POST'])
def AddProduct(name="no_name", descr="no_descr"):
    if request.method == 'POST':
        if request.form["productbtn"] == 'add':     #Add Product to Database
            add_product(cur, name, descr) 
        elif request.form["productbtn"] == 'show':  #Show all Database Object
            show(cur)
    
    product_form = ProductForm(request.form)
    return render_template("add_product.html", form=product_form)


@app.route('/cart', methods=['GET', 'POST'])
def Cart():
    return render_template("cart.html")


