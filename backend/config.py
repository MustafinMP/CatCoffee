import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DB_NAME = os.environ.get('DB_NAME')

HOST = 'localhost'

