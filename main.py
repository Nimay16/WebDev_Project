from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import sqlite3

class Customers(BaseModel):
    cust_id: int | None = None
    name: str
    phone: str

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
async def read_items(id: int, q =None):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("SELECT order_id, notes, timestamp, cust_id FROM orders WHERE order_id=?", (id,))
    order_details = curr.fetchone()
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
    
    if response !=None:
        return response
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/coustomers/")
async def create_customer(customers: Customers):
    if customers.cust_id != None:
        raise HTTPException(status_code=400, detail="cust_id cannot be not null fro post method.")
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("INSERT INTO customers(cust_name, phone) VALUES(?,?)",(customers.name, customers.phone))
    customers.cust_id = curr.lastrowid
    conn.commit()
    conn.close()
    return customers

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


@app.delete("/customers/{cust_del_id}")
async def delete_customer(cust_del_id: int):
    conn = sqlite3.connect("db.sqlite")
    curr = conn.cursor()
    curr.execute("DELETE FROM customers WHERE cust_id = ?",(cust_del_id,))    
    total_changes = conn.total_changes
    conn.commit()
    conn.close()
    if total_changes != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return total_changes