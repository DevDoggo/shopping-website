
import os
import sqlite3

dbpath= os.path.dirname(os.path.abspath(__file__))
db = dbpath + "/products.db"

connection = sqlite3.connect(db)
cur = connection.cursor()

def connect():
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name text, description text)")
    connection.commit()
    print(cur)

def add_product(name, description):
    cur.execute("INSERT INTO products VALUES (NULL, ?, ?)", (name, description))
    print(cur)

def show():
    cur.execute("SELECT name, description FROM products")
    rows = cur.fetchall()
    print(rows)
