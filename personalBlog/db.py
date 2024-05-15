from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
myDataBase = SQLAlchemy()
db_name = '../instance/blog.db'

class User(myDataBase.Model):
    __tablename__ = 'USER_INFO'
    user_id = myDataBase.Column(myDataBase.Integer, primary_key=True)
    email = myDataBase.Column(myDataBase.String(80), nullable=False)
    password = myDataBase.Column(myDataBase.String(80), nullable=False)

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    myDataBase.init_app(app)
    
def index():
        try:
            users = myDataBase.session.execute(myDataBase.select(User).scalar())
            
            user_text = '<ul>'
            for user in users:
                user_text += '<li>' + user.user_id + ', ' + user.user_name + '</li>'
            user_text += '</ul>'
            return users
        except Exception as e:
            # e holds description of the error
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is broken.</h1>'
            return hed + error_text