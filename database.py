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
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, description text, cost integer)")
    #User Table
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)")
    #Cart Table
    cur.execute("CREATE TABLE IF NOT EXISTS carts (id INTEGER PRIMARY KEY AUTOINCREMENT, owner text)")
    
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

def search_product(search, cur):
    cur.execute("SELECT id, name, description from products where id LIKE '%" + search + "%' or name LIKE '%" + search + "%' or description LIKE '%" + search + "%';")
    rows = cur.fetchall()
    return rows

def search_product_by_id(prod_id, cur):
    cur.execute("SELECT " + all_columns +" from products where id = '" + prod_id + "';")
    rows = cur.fetchall()
    return rows

#====================================================================================================
#==================================== Users =========================================================

def add_user(cur):
    pass




#====================================================================================================
#==================================== Carts =========================================================
