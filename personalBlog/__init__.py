from flask import Flask,redirect,url_for,render_template,request,session,flash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from personalBlog.route import auth
app.register_blueprint(auth, url_prefix='/auth')

from . import db
db.init_db(app)


# class Post(db.Model):
#     __tablename__ = 'POST'
#     post_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
#     user_id: Mapped[int] = mapped_column(String(30), nullable=True)
#     title: Mapped[str] = mapped_column(String(30), nullable=True)
#     content: Mapped[str] = mapped_column(String(30), nullable=True)
#     tag: Mapped[str] = mapped_column(String(30), nullable=True)
#     time: Mapped[str] = mapped_column(String(30), nullable=True)




# @app.route('/index')
# def index():
#     users = User.query.all()  # get all rows from USER_INFO table
#     return render_template('index.html', users=users, sayHello='Hello World!')    
# @app.route('/insert')
# def insert():
#     new_user = User(user_id='123', email = '12@gmail.com', password = '123')
#     db.session.add(new_user)
#     db.session.commit()
#     return None

@app.route('/home', methods=['POST', 'GET'])
def home():
    posts = 0
    #posts=Post.query.all()
    return render_template('HomePage.html',posts=posts)

@app.route('/article', methods=['POST', 'GET'])
def article():
    return render_template('ArticlePage.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('AboutPage.html')