import sqlite3
from config import Config

DB_PATH = Config.DB_PATH

def get_db_connection():
    """ Establish connection with SQLite3 DB"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Get the columns by name
    return conn

# <--------------- users table --------------->

def insert_new_user(username: str, password: str, email: str):
    """ Insert a new user """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', (username, password, email, 'user'))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def remove_user(email: str):
    """ Remove a user """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE email = ?', (email,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_user_login(username, password):
    """ Get user by username and password """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        return user if user else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

# <--------------- devices table --------------->

def get_all_tags():
    """ Get all tags from devices table """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM devices')
        tags = set([row[0] for row in cursor.fetchall()])
        return tags if tags else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_devices_by_userid(user_id: int):
    """ Get all devices from a user """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        devices = cursor.execute('SELECT * FROM devices WHERE user_id = ?', (user_id,)).fetchall()
        return devices
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_device(user_id: int, name: str, tag: str, mac: str):
    """ Insert a new device """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO devices (user_id, name, mac, tag) VALUES (?, ?, ?, ?)', (user_id, name, mac, tag))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def remove_device(tag: str):
    """ Remove a device """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM devices WHERE tag = ?', (tag, ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_mac_by_tag(tag: str):
    """ Get mac address by tag """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        mac = cursor.execute('SELECT mac FROM devices WHERE tag = ?', (tag, )).fetchone()
        return mac[0] if mac else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()