from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from flask_login import login_user

from .database import add_product, show_products, get_all_products, search_product, search_product_by_id, add_tests, add_user, get_user, get_all_users 
from .forms import ProductForm, SearchForm, LoginForm
from .app import conn, cur, login_manager

blueprint = Blueprint('standard', __name__)


@blueprint.route('/')
def Default():
    show_products(cur)
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
    username = get_logged_in_user()
    if username != "admin":
        return "Only Admins are allowed to use this page!\
                <a href='/login'>Login</a>"
    
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


@blueprint.route('/cart', methods=['GET', 'POST'])
def Cart():
    username = get_logged_in_user()
    if username != None:
        return render_template("cart.html", user=username)
    else:
        return "<p>You are not logged in!</p> \
                <a href='\nlogin'>Login</a>"


@blueprint.route('/login', methods=['GET', 'POST'])
def Login(): 
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if request.form["loginbtn"] == "login":
            user = get_user(cur, username, password)
            if user != None:
                session['username'] = request.form['username']
                flash('Successfully logged in!')
                return redirect(url_for('standard.Products')) 
            else: 
                flash('Incorrect login!')
                print('incorrect login!')
                #return redirect(url_for('standard.Login'))

        elif request.form["loginbtn"] == "create":
            add_user(cur, username, password)
            conn.commit()
            flash('User was successfully created!')
            #return redirect(url_for('standard.Login'))

        elif request.form["loginbtn"] == "show":
            get_all_users(cur)

    login_form = LoginForm(request.form)
    username = get_logged_in_user()
    return render_template("login.html", form=login_form, user=username)

@blueprint.route('/logout', methods=['GET'])
def logout():
   session.pop('username', None)
   return redirect(url_for('standard.Products'))



#/////// Helper Functions

def get_logged_in_user():
    print (session)
    if 'username' in session:
        return session['username']
    else:
        return None

