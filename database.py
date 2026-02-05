import sqlite3

conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Customer table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    city TEXT,
    join_date TEXT
)
""")

# Product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL
)
""")

# Orders table (renamed from Order)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
)
""")

# Order items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
)
""")

customers = [
    ('Aadi Kalra', 'aadi@gmail.com', 'Delhi', '2024-01-10'),
    ('Rohit Sharma', 'rohit@gmail.com', 'Mumbai', '2024-02-15'),
    ('Ananya Singh', 'ananya@gmail.com', 'Bangalore', '2024-03-05'),
    ('Kunal Verma', 'kunal@gmail.com', 'Pune', '2024-03-20'),
    ('Neha Gupta', 'neha@gmail.com', 'Jaipur', '2024-04-01')
]

cursor.executemany(
    "INSERT INTO Customer (name, email, city, join_date) VALUES (?, ?, ?, ?)",
    customers
)
products = [
    ('Laptop', 'Electronics', 75000),
    ('Smartphone', 'Electronics', 30000),
    ('Headphones', 'Accessories', 2000),
    ('Keyboard', 'Accessories', 1500),
    ('Book', 'Education', 500)
]

cursor.executemany(
    "INSERT INTO Product (name, category, price) VALUES (?, ?, ?)",
    products
)

orders = [
    (1, '2024-04-05', 77000),
    (2, '2024-04-06', 30000),
    (3, '2024-04-07', 3500),
    (4, '2024-04-08', 1500),
    (5, '2024-04-09', 500)
]

cursor.executemany(
    "INSERT INTO Orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)",
    orders
)

order_items = [
    (1, 1, 1, 75000),
    (1, 3, 1, 2000),
    (2, 2, 1, 30000),
    (3, 3, 1, 2000),
    (3, 4, 1, 1500)
]

cursor.executemany(
    """
    INSERT INTO Order_Items (order_id, product_id, quantity, subtotal)
    VALUES (?, ?, ?, ?)
    """,
    order_items
)

conn.commit()
conn.close()
print("database stored")
