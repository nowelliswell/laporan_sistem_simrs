import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings - use app/static/uploads for Railway
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Fix Heroku postgres URL (postgres:// -> postgresql://)
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = uri or Config.SQLALCHEMY_DATABASE_URI
    
    # Security
    SESSION_COOKIE_SECURE = False  # Set to True only if using HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False