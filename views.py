from flask import Blueprint, render_template, request

from .database import add_product, show, get_all, search_product, search_by_id #, get_new_id
from .forms import ProductForm, SearchForm
from .app import conn, cur

blueprint = Blueprint('standard', __name__)


@blueprint.route('/')
def Default():
    show(cur)
    return render_template("default.html")


@blueprint.route('/products', methods=['GET', 'POST'])
@blueprint.route('/products/<prod_id>', methods=['GET', 'POST'])
def Products(prod_id=None):
    search_form = SearchForm(request.form)
    if request.method == 'POST' and request.form["search"] != '':
        search = request.form["search"]
        search_products = search_product(search, cur)
        products = search_products
        return render_template("products.html", products=products, form=search_form)
    
    products = get_all(cur)
    if (prod_id == None):
        return render_template("products.html", products=products, form=search_form)
    else:
        product = search_by_id(prod_id, cur)
        if len(product) > 0 :
            product = product[0]
        else:
            product = ""
        return render_template("products.html", prod_id=prod_id, product=product, products=products, form=search_form) 


@blueprint.route('/add', methods=['GET', 'POST'])
@blueprint.route('/add/<name>', methods=['GET', 'POST'])
def AddProduct(name="no_name", description="no_description"):
    if request.method == 'POST': # and request.form[""]:
        if request.form["productbtn"] == 'add':     #Add Product to Database
            inp = request.form
            name = inp["name"]
            description = inp["description"]
            add_product(cur, name, description)
            conn.commit()
        elif request.form["productbtn"] == 'show':  #Show all Database Object
            show(cur)
    
    product_form = ProductForm(request.form)
    return render_template("add_product.html", form=product_form)


@blueprint.route('/cart', methods=['GET', 'POST'])
def Cart():
    return render_template("cart.html")

