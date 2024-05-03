from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import time
import sqlite3

class Customers(BaseModel):
    cust_id: int | None = None
    name: str
    phone: str

class Item(BaseModel):
    item_id: int | None = None
    item_name: str
    price: float

class Order(BaseModel):
    order_id: int | None = None
    timestamp: int | None = None
    customer_name: str | None = None
    customer_phone: str | None = None
    item_name: List[str]
    notes: str | None = None

app = FastAPI()

@app.get("/")
async def root():
    return{"message":"Hello world"}

@app.get("/customers/{id}")
async def read_customers(id: int, q =None):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT cust_id, cust_name, phone FROM customers WHERE cust_id=?", (id,))
    customer = curr.fetchone()
    conn.close()

    if(customer != None):
        return Customers(cust_id= customer[0], name = customer[1], phone = customer[2])
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/{id}")
async def read_items(id: int, q =None):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT item_id, item_name, price FROM items WHERE item_id=?", (id,))
    item = curr.fetchone()
    conn.close()

    if(item != None):
        return{
            "id": item[0],
            "name": item[1],
            "price": item[2]
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/oders/{id}")
async def read_order(id: int, q =None):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT order_id, notes, timestamp, cust_id FROM orders WHERE order_id=?", (id,))
    order_details = curr.fetchone()
    if order_details != None:
        curr.execute("SELECT cust_id, cust_name, phone FROM customers WHERE cust_id=?", (order_details[3],))
        order_cust = curr.fetchone()
        curr.execute("SELECT item_id FROM order_list WHERE order_id=?", (id,))
        item_ids = curr.fetchall()
        items = []
        for item_id in item_ids:
            curr.execute("SELECT item_id, item_name, price FROM items WHERE item_id=?", (item_id[0],))
            item = curr.fetchone()
            if item:
                items.append({
                    "item_id": item[0],
                    "item_name": item[1],
                    "price": item[2]
                })
        conn.close()
        response = {
            "id": order_details[0],
            "Customer Name": order_cust[1],
            "Customer Phone": order_cust[2],
            "items": items,
            "notes": order_details[1],
            "timestamp": order_details[2]
        }
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/coustomers/")
async def create_customer(customers: Customers):
    if customers.cust_id != None:
        raise HTTPException(status_code=400, detail="cust_id cannot be not null for post method.")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("INSERT INTO customers(cust_name, phone) VALUES(?,?)",(customers.name, customers.phone))
    customers.cust_id = curr.lastrowid
    conn.commit()
    conn.close()
    return customers

@app.post("/items/")
async def create_item(items: Item):
    if items.item_id != None:
        raise HTTPException(status_code=400, detail="item_id cannot be not null for post method.")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("INSERT INTO items(item_name, price) VALUES(?,?)",(items.item_name, items.price))
    items.item_id = curr.lastrowid
    conn.commit()
    conn.close()
    return items

@app.post("/orders/")
async def create_order(orders: Order):
    if orders.order_id != None:
        raise HTTPException(status_code=400, detail="order_id cannot be not null for post method.")
    if orders.timestamp != None:
        raise HTTPException(status_code=400, detail="timestamp cannot be not null.")
    timestamp = int(time.time())
    orders.timestamp = timestamp
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    item_details = []
    for item in orders.item_name:
        curr.execute("SELECT item_id FROM items WHERE item_name=?", (item,))
        items = curr.fetchone()
        if items is None:
            conn.close()
            raise HTTPException(status_code=404, detail="Item not found")
        else:
            item_details.append(items[0])
    curr.execute("SELECT cust_id, cust_name, phone FROM customers WHERE phone =?",(orders.customer_phone,))
    cust_details = curr.fetchone()
    if cust_details is not None:
        curr.execute("INSERT INTO orders(notes, timestamp, cust_id) VALUES(?,?,?)",(orders.notes, orders.timestamp,cust_details[0]))
        order_id = curr.lastrowid
    else:
        curr.execute("INSERT INTO customers(cust_name, phone) VALUES(?,?)",(orders.customer_name, orders.customer_phone))
        cust_id = curr.lastrowid
        curr.execute("INSERT INTO orders(notes, timestamp, cust_id) VALUES(?,?,?)",(orders.notes, orders.timestamp,cust_id))
        order_id = curr.lastrowid
    for item_id in item_details:
        curr.execute("INSERT INTO order_list(order_id,item_id) VALUES(?,?)",(order_id,item_id))
    orders.order_id = order_id
    conn.commit()
    conn.close()
    return orders

@app.put("/customers/{cust_id}")
async def update_customer(cust_id: int, customers: Customers):
    if customers.cust_id != None and customers.cust_id != cust_id:
        raise HTTPException(status_code=400, detail="Customer Id does not match Id in the path")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT cust_id FROM customers WHERE cust_id = ?",(cust_id,))
    id = curr.fetchone()
    if (id != None):
        curr.execute("UPDATE customers SET cust_name =? , phone=? WHERE cust_id=?",(customers.name, customers.phone,cust_id))    
        conn.commit()
        conn.close()
        customers.cust_id = cust_id
        return customers
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, items: Item):
    if items.item_id != None and items.item_id != item_id:
        raise HTTPException(status_code=400, detail="Item Id does not match Id in the path")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT item_id FROM items WHERE item_id = ?",(item_id,))
    id = curr.fetchone()
    if (id != None):
        curr.execute("UPDATE items SET item_name =? , price=? WHERE item_id=?",(items.item_name, items.price,item_id))    
        conn.commit()
        conn.close()
        items.item_id = item_id
        return items
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/orders/{order_id}")
async def update_order(order_id: int,orders: Order):
    if orders.order_id != None and orders.order_id != order_id:
        raise HTTPException(status_code=400, detail="Order Id does not match Id in the path.")
    if orders.timestamp != None or orders.customer_name != None or orders.customer_phone != None:
        raise HTTPException(status_code=400, detail="Timestamp or Customer name and Phone number cannot be changed.")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    item_details = []
    for item in orders.item_name:
        curr.execute("SELECT item_id FROM items WHERE item_name=?", (item,))
        items = curr.fetchone()
        if items is None:
            conn.close()
            raise HTTPException(status_code=404, detail="Item not found")
        else:
            item_details.append(items[0])
        curr.execute("UPDATE orders SET notes=?",(orders.notes,))
        orders.order_id = order_id
    for item_id in item_details:
        curr.execute("DELETE FROM order_list WHERE order_id = ?",(order_id,))
        curr.execute("INSERT INTO order_list(order_id,item_id) VALUES(?,?)",(order_id,item_id))
    orders.order_id = order_id
    item_names=[]
    for items in orders.item_name:
        item_names.append(items)
    reponse={
        "order_id":orders.order_id,
        'items_name':item_names,
        'notes':orders.notes
    }
    conn.commit()
    conn.close()
    return reponse

@app.delete("/customers/{cust_del_id}")
async def delete_customer(cust_del_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM customers WHERE cust_id = ?",(cust_del_id,))
    total_changes = conn.total_changes
    curr.execute("SELECT order_id FROM orders WHERE cust_id = ?",(cust_del_id,))
    order_id = curr.fetchall()
    for order in order_id:
        curr.execute("DELETE FROM order_list WHERE order_id = ?",(order))
    curr.execute("DELETE FROM orders WHERE cust_id = ?",(cust_del_id,))
    conn.commit()
    conn.close()
    if total_changes ==0:
        raise HTTPException(status_code=404, detail="Item not found")
    return total_changes

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM items WHERE item_id = ?",(item_id,))
    total_changes = conn.total_changes
    curr.execute("DELETE FROM order_list WHERE item_id = ?",(item_id,))
    conn.commit()
    conn.close()
    if total_changes ==0:
        raise HTTPException(status_code=404, detail="Item not found")
    return total_changes

@app.delete("/order/{order_id}")
async def delete_order(order_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM orders WHERE order_id = ?",(order_id,))
    total_changes = conn.total_changes
    curr.execute("DELETE FROM order_list WHERE order_id = ?",(order_id,))
    conn.commit()
    conn.close()
    if total_changes ==0:
        raise HTTPException(status_code=404, detail="Item not found")
    return total_changes