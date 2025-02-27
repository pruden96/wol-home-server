import sqlite3


def create_db() -> None:
    conn = sqlite3.connect("database/home_server.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL
                )""")

    c.execute("""CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    tag TEXT NOT NULL UNIQUE,
                    mac TEXT,
                    ip TEXT,
                    type TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    CHECK (mac IS NOT NULL OR ip IS NOT NULL)
                )""")

    conn.commit()
    conn.close()


create_db()
