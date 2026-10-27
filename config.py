import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ensure database directory exists
db_dir = os.path.join(BASE_DIR, 'database')
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, 'alumni.db').replace('\\', '/')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'alumniconnect-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
