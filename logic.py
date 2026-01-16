import sqlite3

DB_NAME = "assets.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            brand TEXT,
            status TEXT,
            purchase_date TEXT
        )
    """)
    conn.commit()
    return conn

def add_asset(asset):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO assets (name, type, brand, status, purchase_date) VALUES (?, ?, ?, ?, ?)",
        (asset.name, asset.asset_type, asset.brand, asset.status, asset.purchase_date)
    )
    conn.commit()
    conn.close()

def delete_asset(asset_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    conn.commit()
    conn.close()

def search_asset(asset_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
    data = cur.fetchone()
    conn.close()
    return data

def fetch_all_assets():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assets")
    data = cur.fetchall()
    conn.close()
    return data

def dashboard_counts():
    conn = connect_db()
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
