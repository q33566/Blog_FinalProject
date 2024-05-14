from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
db = SQLAlchemy()
db_name = '../instance/blog.db'

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)