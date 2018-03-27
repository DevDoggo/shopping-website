import os
import sqlite3




entries = [['FirstToy', 'This is our first product.', '225'],
        ['SecondToy', 'Second product to our firm!', '775'],
        ['ThirdToy', 'This is not made for children. Run.', '420'],
        ['FourthToy', "We're about to go bankrupt, sadly.", '69']]

all_columns = "id, name, description, cost"

def add_tests(cur):
    for x in entries:
        nm = x[0]
        dc = x[1]
        cs = x[2]
        cur.execute("INSERT INTO products VALUES (NULL, ?, ?, ?)", (nm, dc, cs))

def connect(db):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    #Product Table
    cur.execute("CREATE TABLE IF NOT EXISTS products \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, description text, cost integer)")
    #User Table
    cur.execute("CREATE TABLE IF NOT EXISTS users \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)")
    #Cart Table
#    cur.execute("CREATE TABLE IF NOT EXISTS carts \
#            (id INTEGER PRIMARY KEY AUTOINCREMENT, owner text)")
    
    connection.commit()
    return(connection, cur)

#====================================================================================================
#==================================== Products ======================================================
def add_product(cur, name, description, cost):
    cur.execute("INSERT INTO products VALUES (NULL, ?, ?, ?)", (name, description, cost))
    print(cur)

def show_products(cur):
    cur.execute("SELECT " + all_columns + " FROM products")
    rows = cur.fetchall()
    print(rows)

def get_all_products(cur):
    cur.execute("SELECT " + all_columns + " FROM products")
    rows = cur.fetchall()
    return rows

def search_product(cur, search):
    cur.execute("SELECT id, name, description, cost from products where id LIKE '%" + search + "%' or name LIKE '%" + search + "%' or description LIKE '%" + search + "%';")
    rows = cur.fetchall()
    return rows

def search_product_by_id(cur, prod_id):
    cur.execute("SELECT " + all_columns +" from products where id = '" + prod_id + "';")
    rows = cur.fetchall()
    return rows

def remove_product(cur, prod_id):
    cur.execute("DELETE FROM products WHERE id = " + prod_id + ";")
    users = get_all_users(cur)
    print(users)
    for user in users:
        username = user[0]
        print(username)
        remove_from_cart(cur, str(username), prod_id)


#====================================================================================================
#==================================== Users =========================================================

def add_user(cur, username, password):
    cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, password))

def get_user(cur, username, password):
    cur.execute("SELECT username from users where username = '" + username + "' and password = '" + password + "';")
    rows = cur.fetchall()
    if len(rows) != 0:
        return rows[0]
    else: 
        return None

def get_all_users(cur):
    cur.execute("SELECT username, password from users")
    rows = cur.fetchall()
    return(rows)

#====================================================================================================
#==================================== Carts =========================================================

def create_cart(cur, username):
    cur.execute("CREATE TABLE IF NOT EXISTS " + username + "_cart \
            (id int, name text, description text, cost integer )")

def add_to_cart(cur, username, product):
    cur.execute("INSERT INTO "+ username + "_cart VALUES (?, ?, ?, ?)", (product[0], product[1], product[2], product[3]))

def get_cart(cur, username):
    cur.execute("SELECT id, name, description, cost FROM " + username + "_cart")
    rows = cur.fetchall()
    return rows

def remove_from_cart(cur, username, prod_id):
    cur.execute("DELETE FROM " + username + "_cart WHERE id = " + prod_id + ";")



def show_tables(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    print(rows)

