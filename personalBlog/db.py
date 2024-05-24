from flask_sqlalchemy import SQLAlchemy
DB_NAME = 'blog.db'
db = SQLAlchemy()
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)