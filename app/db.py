import os
import sqlite3
from pathlib import Path

def get_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str):
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create tables
    c.executescript('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        is_public INTEGER NOT NULL CHECK (is_public IN (0,1))
    );
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    );
    ''')
    # Seed data if empty
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        products = [
            ("Python Basics", 10.0, "books", 1),
            ("Flask Cookbook", 15.0, "books", 1),
            ("Smartphone X", 299.0, "electronics", 1),
            ("INTERNAL Prototype X", 0.0, "books", 0),
            ("INTERNAL Supplier List", 0.0, "books", 0),
        ]
        c.executemany('INSERT INTO products (name, price, category, is_public) VALUES (?,?,?,?)', products)
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        c.execute('INSERT INTO users (username, password_hash) VALUES (?,?)',
                  ("demo", generate_password_hash("demo123")))
    conn.commit()
    conn.close()
