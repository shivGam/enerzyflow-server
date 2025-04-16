from app.db import get_db_connection
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

faker = Faker()

try:
    conn = get_db_connection()
    conn.autocommit = True
    cur = conn.cursor()
    print("Connection to PostgreSQL database established successfully.")
except Exception as e:
    print("Connection to PostgreSQL database failed:", str(e))

tables = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age INT,
            signup_date DATE
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10,2),
            in_stock BOOLEAN,
            created_at TIMESTAMP
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT,
            product_id INT,
            quantity INT,
            order_date DATE
        );
    """,
    "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            user_id INT,
            product_id INT,
            rating INT,
            review_text TEXT
        );
    """,
    "payments": """
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            order_id INT,
            amount DECIMAL(10,2),
            payment_method VARCHAR(50),
            payment_date TIMESTAMP
        );
    """
}

for table_name, create_query in tables.items():
    cur.execute(create_query)
    print(f"✅ Table '{table_name}' created successfully!")

def insert_dummy_users():
    for _ in range(10):
        cur.execute("""
            INSERT INTO users (name, email, age, signup_date)
            VALUES (%s, %s, %s, %s);
        """, (faker.name(), faker.email(), faker.random_int(min=18, max=65), faker.date_this_decade()))

def insert_dummy_products():
    for _ in range(10):
        cur.execute("""
            INSERT INTO products (name, price, in_stock, created_at)
            VALUES (%s, %s, %s, %s);
        """, (faker.word(), round(faker.pydecimal(left_digits=3, right_digits=2, positive=True), 2),
              faker.boolean(), datetime.now()))

def insert_dummy_orders():
    for _ in range(10):
        cur.execute("""
            INSERT INTO orders (user_id, product_id, quantity, order_date)
            VALUES (%s, %s, %s, %s);
        """, (faker.random_int(min=1, max=10), faker.random_int(min=1, max=10),
              faker.random_int(min=1, max=5), faker.date_this_year()))

def insert_dummy_reviews():
    for _ in range(10):
        cur.execute("""
            INSERT INTO reviews (user_id, product_id, rating, review_text)
            VALUES (%s, %s, %s, %s);
        """, (faker.random_int(min=1, max=10), faker.random_int(min=1, max=10),
              faker.random_int(min=1, max=5), faker.text()))

def insert_dummy_payments():
    for _ in range(10):
        cur.execute("""
            INSERT INTO payments (order_id, amount, payment_method, payment_date)
            VALUES (%s, %s, %s, %s);
        """, (faker.random_int(min=1, max=10),
              round(faker.pydecimal(left_digits=4, right_digits=2, positive=True), 2),
              faker.random_element(elements=("Credit Card", "PayPal", "Bank Transfer")),
              datetime.now()))

# Run all insert functions
insert_dummy_users()
insert_dummy_products()
insert_dummy_orders()
insert_dummy_reviews()
insert_dummy_payments()

print("Job performed")

cur.close()
conn.close()
print("connection closed")
