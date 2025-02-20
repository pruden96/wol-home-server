import sqlite3
import bcrypt
import logging
from config import Config

# Configurar logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = Config.DB_PATH

def get_db_connection():
    """ Establish connection with SQLite3 DB"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Get the columns by name
    return conn

def hash_password(password: str) -> str:
    """ Hash password securely """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(hashed_password: str, password: str) -> bool:
    """ Verify password hash """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# <--------------- users table --------------->

def insert_new_user(username: str, password: str, email: str) -> None:
    """ Insert a new user securely """
    hashed_password = hash_password(password)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', 
                           (username, hashed_password, email, 'user'))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def remove_user(email: str) -> None:
    """ Remove a user """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE email = ?', (email,))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def get_user_login(username: str, password: str) -> tuple:
    """ Get user by username and validate password """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user and check_password(user['password'], password):
                return user
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    return None

def get_user_by_username(username: str) -> tuple:
    """ Get user by username """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM users WHERE username = ?', (username, )).fetchone()
            return result if result else None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def get_user_by_email(email: str) -> tuple:
    """ Get user by email """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT * FROM users WHERE email = ?', (email, )).fetchone()
            return result if result else None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

# <--------------- devices table --------------->

def get_all_tags() -> list:
    """ Get all tags from devices table """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT tag FROM devices')
            return {row[0] for row in cursor.fetchall()} or None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def get_devices_by_userid(user_id: int) -> list:
    """ Get all devices from a user """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            return cursor.execute('SELECT * FROM devices WHERE user_id = ?', (user_id,)).fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def insert_device(user_id: int, name: str, tag: str, mac: str) -> None:
    """ Insert a new device """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO devices (user_id, name, mac, tag) VALUES (?, ?, ?, ?)', (user_id, name, mac, tag))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def remove_device(tag: str) -> None:
    """ Remove a device """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM devices WHERE tag = ?', (tag,))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def get_mac_by_tag(tag: str) -> str:
    """ Get MAC address by tag """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            mac = cursor.execute('SELECT mac FROM devices WHERE tag = ?', (tag,)).fetchone()
            return mac[0] if mac else None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
