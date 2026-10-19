import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-secret-key')
    # 相對路徑的 sqlite 會由 Flask-SQLAlchemy 放進 instance/ 資料夾
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_SUBDIR = 'uploads'


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
