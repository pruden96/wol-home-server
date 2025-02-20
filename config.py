import os
from dotenv import load_dotenv

# Load enviroment variables from .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    AUTH_KEY = os.getenv('AUTH_KEY')
    DB_PATH = os.getenv('DB_PATH')
    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_AUTH = os.getenv('ADMIN_AUTH')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

