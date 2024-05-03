# Web Development Project: Online Ordering System

## Overview
This FastAPI application serves as a backend for an online ordering system. It handles operations for managing customers, items, and orders through a SQLite database. The API allows for CRUD (Create, Read, Update, Delete) operations on these resources.

## Features
- Manage customers, items, and orders.
- Robust error handling for data consistency.
- Simple and intuitive endpoints for easy interaction with the frontend or other clients.

## Technology Stack
- **FastAPI**: Asynchronous framework for building APIs.
- **SQLite**: Database to store and retrieve data.
- **Pydantic**: Data validation by using Python type annotations.

## Installation

To get this project up and running locally, follow these steps:

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Nimay16/WebDev_Project.git
   
   cd WebDev_Project

2. Install the required packages:
    `pip install fastapi[all] sqlite3 pydantic`

3. Initialize the database:
    ```python init_db.py```

4. Start the server:
    ```uvicorn main:app --reload```

### API Endpoints
1. General:
- `GET /` : Test endpoint to check if the API is running.

2. Customer Management:
- `POST /customers/` : Create a new customer(customer ID should not be provided as it's auto-generated).
- `GET /customers/{id}` : Retrieve a customer by ID.
- `PUT /customers/{cust_id}` : Update a customer by ID(cannot change customer ID).
- `DELETE /customers/{cust_del_id}` : Delete a customer by ID.

3. Item Management:
- `POST /items/` : Create a new item(item ID should not be provided as it's auto-generated).
- `GET /items/{id}` : Retrieve an item by ID.
- `PUT /items/{item_id}` : Update an item by ID(cannot change item ID).
- `DELETE /items/{item_id}` : Delete an item by ID.

4. Order Management:
- `POST /orders/` : Create a new order(Oorder ID and timestamp are auto-generated).
- `GET /orders/{id}` : Retrieve an order by ID.
- `PUT /orders/{order_id}` : Update an order by ID(order ID, timestamp, customer name, and phone number cannot be changed).
- `DELETE /order/{order_id}` : Delete an order by ID.

### Contact Information
- Nimay Shah