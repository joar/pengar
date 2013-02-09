import os

APP_DIR = __file__

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///pengar.sqlite')
SQLALCHEMY_DATABASE_URI = DATABASE_URL

# WWW
PORT = int(os.environ.get('PORT', 5003))
DEBUG = bool(int(os.environ.get('DEBUG', 1)))
