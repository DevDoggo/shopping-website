import os
import sqlite3

#dbpath= os.path.dirname(os.path.abspath(__file__))
#db = dbpath + "/products.db"

#connection = sqlite3.connect(db)
#cur = connection.cursor()

entries = [['FirsToy', 'This is our first product.', '225'],
        ['SecondToy', 'Second product to our firm!', '775'],
        ['ThirdToy', 'This is not made for children. Run.', '420']]

all_columns = "id, name, description, cost, url"

def add_tests(cur):
    for x in entries:
        nm = x[0]
        dc = x[1]
        cs = x[2]
        
        url = "/products/9"  
        cur.execute("INSERT INTO products VALUES (NULL, ?, ?, ?, ?)", (nm, dc, cs, url))



def connect(db):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, description text, cost integer, url text)")
    connection.commit()
    return(connection, cur)

def add_product(cur, name, description, cost):
    cur.execute("INSERT INTO products VALUES (NULL, ?, ?, ?, ?)", (name, description, cost, url))
    print(cur)

def show(cur):
    cur.execute("SELECT " + all_columns + " FROM products")
    rows = cur.fetchall()
    print(rows)

def get_all(cur):
    cur.execute("SELECT " + all_columns + " FROM products")
    rows = cur.fetchall()
    return rows

def search_product(search, cur):
    cur.execute("SELECT id, name, description from products where id LIKE '%" + search + "%' or name LIKE '%" + search + "%' or description LIKE '%" + search + "%';")
    rows = cur.fetchall()
    return rows

def search_by_id(prod_id, cur):
    cur.execute("SELECT " + all_columns +" from products where id = '" + prod_id + "';")
    rows = cur.fetchall()
    return rows



