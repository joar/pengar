import os

APP_DIR = __file__

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///pengar.sqlite')
