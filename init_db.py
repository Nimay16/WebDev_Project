import sqlite3
import json

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
	cust_id INTEGER PRIMARY KEY,
	cust_name CHAR(64) NOT NULL,
	phone CHAR(10) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
	item_id INTEGER PRIMARY KEY,
	item_name CHAR(64) NOT NULL,
	price REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
	order_id INTEGER PRIMARY KEY,
	notes TEXT,
    timestamp INTEGER,
    cust_id INTEGER,
	FOREIGN KEY(cust_id)  REFERENCES customers(cust_id)
    
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_list(
	ol_id INTEGER PRIMARY KEY,
    item_id INTEGER,
    order_id INTGER,
	FOREIGN KEY(item_id) REFERENCES items(item_id),
    FOREIGN KEY(order_id) REFERENCES oders(order_id)
   
);
""")

with open('example_orders.json') as file:
    data = json.load(file)
    

customers = {}
items = {}

for order in data:
    customers[order["phone"]] = order["name"]
    for item in order["items"]:
        items[item["name"]] = item["price"]
    

for phone, name in customers.items():
    cursor.execute("INSERT INTO customers(cust_name, phone) VALUES(?,?)",(name,phone))
    
for name, price in items.items():
    cursor.execute("INSERT INTO items(item_name, price) VALUES(?,?)",(name,price))
    
for order in data:
    cursor.execute("SELECT cust_id FROM customers WHERE phone = ? ",(order["phone"],))
    cust_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO orders (notes, timestamp,cust_id) VALUES(?,?,?)", (order["notes"],order["timestamp"], cust_id))
    order_id = cursor.lastrowid
    for item in order["items"]:
        cursor.execute("SELECT item_id FROM items WHERE item_name = ? ",(item["name"],))
        item_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO order_list(order_id, item_id) VALUES(?,?)",(order_id, item_id))
    
connection.commit()
connection.close()


