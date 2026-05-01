"""
=============================================================
 database.py - SQLite setup for ennojoum
=============================================================
 - Creates the database file (ennojoum.db) if it doesn't exist
 - Creates tables: cars, employees
 - Inserts default employee (admin1 / 1234)
=============================================================
"""

import sqlite3
import os

DB_NAME = "ennojoum.db"


def get_db_connection():
    """
    Open a connection to the SQLite database.
    row_factory = sqlite3.Row lets us access columns by name (like a dict).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize the database:
    - Create tables if they don't already exist
    - Add the default employee (admin1 / 1234)
    """
    first_time = not os.path.exists(DB_NAME)

    conn = get_db_connection()
    cur  = conn.cursor()

    # ---------- cars table ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            code      TEXT    UNIQUE NOT NULL,
            car_type  TEXT    NOT NULL,
            phone     TEXT    NOT NULL,
            wash_type TEXT    NOT NULL,
            price     INTEGER NOT NULL,
            status    TEXT    NOT NULL DEFAULT 'Started',
            date      TEXT    NOT NULL
        )
    """)

    # ---------- employees table ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL
        )
    """)

    # ---------- default employee ----------
    cur.execute("SELECT id FROM employees WHERE username = 'admin1'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO employees (username, password) VALUES (?, ?)",
            ("admin1", "1234")
        )

    conn.commit()
    conn.close()

    if first_time:
        print("[DB] Database created successfully (ennojoum.db)")
    else:
        print("[DB] Database ready.")


# Allow running this file directly to (re)initialize the DB
if __name__ == "__main__":
    init_db()
