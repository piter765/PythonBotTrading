import sqlite3
from datetime import datetime

DB_NAME = "trading_bot.db"

class Database:
    def __init__(self):
        """Initialize database connection and create tables if they don't exist"""
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create orders table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_order(self, symbol, quantity, price):
        """Insert a new order into the database"""
        self.cursor.execute('''
            INSERT INTO orders (symbol, quantity, price) 
            VALUES (?, ?, ?)
        ''', (symbol, quantity, price))
        self.conn.commit()

    def get_open_orders(self):
        """Retrieve all open orders"""
        self.cursor.execute('SELECT * FROM orders WHERE status = "open"')
        return self.cursor.fetchall()

    def update_order_status(self, order_id, new_status):
        """Update the status of an order"""
        self.cursor.execute('''
            UPDATE orders 
            SET status = ? 
            WHERE id = ?
        ''', (new_status, order_id))
        self.conn.commit()

    def close(self):
        """Close database connection"""
        self.conn.close()
