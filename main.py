from fastapi import FastAPI,HTTPException
import sqlite3

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
        return{
            "id": customer[0],
            "name": customer[1],
            "phone": customer[2]
        }
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
   
    raise HTTPException(status_code=404, detail="Item not found")