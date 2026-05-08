"""
=============================================================
 database.py - PostgreSQL setup for Mnojo (Ennoujoum)
=============================================================
 - Connects to PostgreSQL using DATABASE_URL (Railway env var)
 - Falls back to SQLite locally if DATABASE_URL is not set
 - Creates tables: cars, employees, managers
 - Same interface as before: get_db_connection() and init_db()
=============================================================
"""

import os

# ---------------------------------------------------------------
# Detect which database to use.
# Railway injects DATABASE_URL automatically when you add a
# PostgreSQL plugin. Locally it is not set, so we fall back
# to SQLite so you can still test on your laptop.
# ---------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Railway sometimes gives a URL starting with "postgres://"
# but psycopg2 requires "postgresql://". We fix that here.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

USE_POSTGRES = bool(DATABASE_URL)


# ---------------------------------------------------------------
# PgConnectionWrapper
# psycopg2 does not support conn.execute() like sqlite3 does.
# This wrapper adds that method so the rest of app.py works
# WITHOUT any changes at all.
# ---------------------------------------------------------------
class PgConnectionWrapper:
    """Makes psycopg2 connection behave like sqlite3 connection."""

    def __init__(self, raw_conn):
        import psycopg2.extras
        self._conn = raw_conn
        self._cur  = raw_conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    # app.py calls conn.execute(sql, params) everywhere
    def execute(self, sql, params=()):
        sql = sql.replace("?", "%s")   # SQLite uses ?, PostgreSQL uses %s
        self._cur.execute(sql, params)
        return self._cur

    def cursor(self):
        return self._cur

    def commit(self):
        self._conn.commit()

    def close(self):
        try:
            self._cur.close()
        except Exception:
            pass
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ---------------------------------------------------------------
# get_db_connection()
# Single entry point used by app.py everywhere.
# ---------------------------------------------------------------
def get_db_connection():
    if USE_POSTGRES:
        import psycopg2
        raw_conn = psycopg2.connect(DATABASE_URL)
        return PgConnectionWrapper(raw_conn)
    else:
        import sqlite3
        conn = sqlite3.connect("mnojo.db")
        conn.row_factory = sqlite3.Row
        return conn


# ---------------------------------------------------------------
# init_db()
# Creates all tables if they do not exist yet.
# ---------------------------------------------------------------
def init_db():
    conn = get_db_connection()

    if USE_POSTGRES:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id        SERIAL PRIMARY KEY,
                code      TEXT    UNIQUE NOT NULL,
                car_type  TEXT    NOT NULL,
                phone     TEXT    NOT NULL,
                wash_type TEXT    NOT NULL,
                price     INTEGER NOT NULL,
                status    TEXT    NOT NULL DEFAULT 'Started',
                date      TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id       SERIAL PRIMARY KEY,
                username TEXT    UNIQUE NOT NULL,
                password TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS managers (
                id                SERIAL PRIMARY KEY,
                username          TEXT    UNIQUE NOT NULL,
                password          TEXT    NOT NULL,
                status            TEXT    NOT NULL DEFAULT 'pending',
                date              TEXT,
                security_question TEXT,
                security_answer   TEXT
            )
        """)
        # ADD COLUMN IF NOT EXISTS works in PostgreSQL 9.6+
        for col_sql in (
            "ALTER TABLE managers ADD COLUMN IF NOT EXISTS security_question TEXT",
            "ALTER TABLE managers ADD COLUMN IF NOT EXISTS security_answer   TEXT",
        ):
            try:
                conn.execute(col_sql)
            except Exception:
                pass

        conn.commit()
        conn.close()
        print("[DB] PostgreSQL database ready. OK")

    else:
        import sqlite3
        conn.execute("""
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    UNIQUE NOT NULL,
                password TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS managers (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                username          TEXT    UNIQUE NOT NULL,
                password          TEXT    NOT NULL,
                status            TEXT    NOT NULL DEFAULT 'pending',
                date              TEXT,
                security_question TEXT,
                security_answer   TEXT
            )
        """)
        for col_sql in (
            "ALTER TABLE managers ADD COLUMN security_question TEXT",
            "ALTER TABLE managers ADD COLUMN security_answer   TEXT",
        ):
            try:
                conn.execute(col_sql)
            except sqlite3.OperationalError:
                pass

        conn.commit()
        conn.close()
        print("[DB] SQLite database ready (local mode). OK")


if __name__ == "__main__":
    init_db()
