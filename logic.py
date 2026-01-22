import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "assets.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            brand TEXT NOT NULL,
            status TEXT NOT NULL,
            purchase_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_asset(asset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO assets (name, type, brand, status, purchase_date)
        VALUES (?, ?, ?, ?, ?)
    """, (asset.name, asset.asset_type, asset.brand, asset.status, asset.purchase_date))
    conn.commit()
    conn.close()

def delete_asset(asset_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    conn.commit()
    conn.close()

def search_asset(asset_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
    row = cur.fetchone()
    conn.close()
    return row

def fetch_all_assets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assets")
    rows = cur.fetchall()
    conn.close()
    return rows

def dashboard_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM assets")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status='Working'")
    working = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status='In Repair'")
    repair = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status='Disposed'")
    disposed = cur.fetchone()[0]

    conn.close()
    return total, working, repair, disposed
