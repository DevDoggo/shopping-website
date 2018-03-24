from flask import Blueprint, render_template, request, redirect, url_for, session

from .database import add_product, show_products, get_all_products, search_product, search_product_by_id, add_tests 
from .forms import ProductForm, SearchForm, LoginForm
from .app import conn, cur

blueprint = Blueprint('standard', __name__)


@blueprint.route('/')
def Default():
    show(cur)
    return redirect(url_for('standard.Products'))
#    return render_template("default.html")

@blueprint.route('/products', methods=['GET', 'POST'])
@blueprint.route('/products/<prod_id>', methods=['GET', 'POST'])
def Products(prod_id=None):

    username = get_logged_in_user()
    
    search_form = SearchForm(request.form)
    if request.method == 'POST' and request.form["search"] != '':
        search = request.form["search"]
        search_products = search_product(search, cur)
        products = search_products
    else: 
        products = get_all_products(cur)
   

    product = ""
    if (prod_id != None):               # If we don't have a product ID
        product = search_product_by_id(prod_id, cur)
        if len(product) > 0 :
            product = product[0]
        else:
            product = ""
        
    return render_template("products.html", 
                user=username,
                prod_id=prod_id, 
                product=product, 
                products=products, 
                form=search_form) 


@blueprint.route('/add', methods=['GET', 'POST'])
@blueprint.route('/add/<name>', methods=['GET', 'POST'])
def AddProduct(name="no_name", description="no_description"):
    if request.method == 'POST': # and request.form[""]:
        if request.form["productbtn"] == 'add':     #Add Product to Database
            inp = request.form
            name = inp["name"]
            description = inp["description"]
            cost = inp["cost"]
            add_product(cur, name, description, cost)
            conn.commit()
        elif request.form["productbtn"] == 'test':  #Show all Database Object
            add_tests(cur)
            conn.commit()
        elif request.form["productbtn"] == 'show':
            show(cur)
    product_form = ProductForm(request.form)
    return render_template("add_product.html", form=product_form)


@blueprint.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('standard.Products')) 
    else:
        pass 
    login_form = LoginForm(request.form)
    return render_template("login.html", form=login_form)


@blueprint.route('/cart', methods=['GET', 'POST'])
def Cart():
    return render_template("cart.html")


#/////// Helper Functions

def get_logged_in_user():
    print (session)
    if 'username' in session:
        return session['username']
    else:
        return None





