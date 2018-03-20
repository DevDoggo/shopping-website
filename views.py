from flask import Blueprint, render_template, request

from .database import add_product, show
from .forms import ProductForm
from .app import conn, cur

blueprint = Blueprint('standard', __name__)


@blueprint.route('/')
def Default():
    show(cur)
    return render_template("default.html")


@blueprint.route('/products', methods=['GET', 'POST'])
@blueprint.route('/products/<prod_id>', methods=['GET', 'POST'])
def Products(prod_id=None):
    if (prod_id == None):
        return render_template("products.html")
    else:
        return render_template("products.html", prod_id=prod_id) 


@blueprint.route('/add', methods=['GET', 'POST'])
@blueprint.route('/add/<name>', methods=['GET', 'POST'])
def AddProduct(name="no_name", descr="no_descr"):
    if request.method == 'POST':
        if request.form["productbtn"] == 'add':     #Add Product to Database
            add_product(cur, name, descr) 
        elif request.form["productbtn"] == 'show':  #Show all Database Object
            show(cur)
    
    product_form = ProductForm(request.form)
    return render_template("add_product.html", form=product_form)


@blueprint.route('/cart', methods=['GET', 'POST'])
def Cart():
    return render_template("cart.html")

