"""
=============================================================
 database.py - PostgreSQL setup for Mnojo (Ennoujoum)
=============================================================
"""

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
USE_POSTGRES = bool(DATABASE_URL)


class PgConnectionWrapper:
    """Makes psycopg2 connection behave like sqlite3 connection."""

    def __init__(self, raw_conn):
        import psycopg2.extras
        self._conn = raw_conn
        self._cur  = raw_conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    def execute(self, sql, params=()):
        sql = sql.replace("?", "%s")
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_log (
                id      SERIAL PRIMARY KEY,
                phone   TEXT NOT NULL,
                message TEXT NOT NULL,
                time    TEXT NOT NULL,
                code    TEXT,
                link    TEXT
            )
        """)
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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_log (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                phone   TEXT NOT NULL,
                message TEXT NOT NULL,
                time    TEXT NOT NULL,
                code    TEXT,
                link    TEXT
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
