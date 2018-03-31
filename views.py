from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from flask_login import login_user

from . import database as db

#from .database import add_product, show_products, get_all_products, search_product, search_product_by_id, remove_product, add_tests, add_user, get_user, get_all_users, create_cart, add_to_cart, get_cart, show_tables, remove_from_cart, edit_product

from .forms import ProductForm, SearchForm, LoginForm
from .app import conn, cur, login_manager

blueprint = Blueprint('standard', __name__)


@blueprint.route('/')
def Default():
    db.show_products(cur)
    return redirect(url_for('standard.Products'))

@blueprint.route('/products', methods=['GET', 'POST'])
@blueprint.route('/products/<prod_id>', methods=['GET', 'POST'])
def Products(prod_id=None):
    username = get_logged_in_user() 
    search_form = SearchForm(request.form)
    products = db.get_all_products(cur)
    
    if request.method == 'POST':
        if "search_btn" in request.form and search_form.validate():
            search = request.form["search"]
            products = db.search_product(cur, search)  
        elif "productbtn" in request.form:
            prod = db.search_product_by_id(cur, request.form["productbtn"])
            db.add_to_cart(cur,conn, username, prod) 
            #conn.commit()

    product = None
    if (prod_id != None):               # If we don't have a product ID
        prod = db.search_product_by_id(cur, prod_id)
        product = prod
        
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
    
    products = db.get_all_products(cur)
    product_form = ProductForm(request.form)

    if request.method == 'POST' and product_form.validate(): # and request.form[""]:
        if "addprod_btn" in request.form: 
            name = request.form["name"]
            description = request.form["description"]
            cost = request.form["cost"]
            db.add_product(cur, conn, name, description, cost)
            #conn.commit()
        elif "testprod_btn" in request.form:
            db.add_tests(cur)
            conn.commit() 
        elif "deletebtn" in request.form: 
            db.remove_product(cur, conn, request.form["deletebtn"])
            #conn.commit()
        elif "editbtn" in request.form:
            edit_form = ProductForm(request.form)    
            prod_id = request.form["editbtn"]
            product = db.search_product_by_id(cur, prod_id)[0]
            return render_template("add_product.html", 
                    product=product, 
                    form=product_form, 
                    edit_form=edit_form, 
                    products=products)
        elif "save_edit_btn" in request.form:
            prod_id = request.form["save_edit_btn"]
            name = request.form["name"]
            description = request.form["description"]
            cost = request.form["cost"]
            db.edit_product(cur, conn, prod_id, name, description, cost)
            #conn.commit() 
            products= db.get_all_products(cur)
            
        elif request.method == 'POST':
            print("naaa boii, you need to give some input!")

    return render_template("add_product.html", form=product_form, products=products)


@blueprint.route('/cart', methods=['GET', 'POST'])
def Cart():
    username = get_logged_in_user()
    if username == None:
        return "<p>You are not logged in!</p> \
                <a href='\nlogin'>Login</a>"

    if request.method == "POST" and request.form["productbtn"] != "":
        prod_id = request.form["productbtn"]
        db.remove_from_cart(cur, conn, username, prod_id)
        #conn.commit() 
        
    products = db.get_cart(cur, username)
    product_form = ProductForm()
    return render_template("cart.html", user=username, products=products, form=product_form)
    

@blueprint.route('/login', methods=['GET', 'POST'])
def Login(): 
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if request.form["loginbtn"] == "login":
            user = db.get_user(cur, username, password)
            if user != None:
                session['username'] = request.form['username']
                flash('Successfully logged in!')
                return redirect(url_for('standard.Products')) 
            else: 
                flash('Incorrect login!')

        elif request.form["loginbtn"] == "create":
            db.add_user(cur, conn, username, password)
            db.create_cart(cur, conn, username)
            #conn.commit()

            flash('User was successfully created!')

        elif request.form["loginbtn"] == "show":
            db.get_all_users(cur)

    login_form = LoginForm(request.form)
    username = get_logged_in_user()
    db.show_tables(cur)
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

