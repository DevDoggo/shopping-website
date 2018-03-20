from flask import Flask, render_template, request
import database as db
app = Flask(__name__)


db.connect()


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
def AddProduct(name="namex"):
    if request.method == 'POST':
        if request.form["productbtn"] == 'add':
            db.add_product("namex", "descriptionx")
        elif request.form["productbtn"] == 'show':
            db.show()
    
    return render_template("add_product.html")


@app.route('/cart', methods=['GET', 'POST'])
def Cart():
    return render_template("cart.html")


