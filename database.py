import os
import sqlite3

#dbpath= os.path.dirname(os.path.abspath(__file__))
#db = dbpath + "/products.db"

#connection = sqlite3.connect(db)
#cur = connection.cursor()

def connect(db):
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name text, description text)")
    connection.commit()
    return(connection, cur)

def add_product(cur, name, description):
    cur.execute("INSERT INTO products VALUES (NULL, ?, ?)", (name, description))
    print(cur)

def show(cur):
    cur.execute("SELECT name, description FROM products")
    rows = cur.fetchall()
    print(rows)
