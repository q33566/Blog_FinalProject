from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from flask import flash
import re
DB_NAME = 'blog.db'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    __tablename__  = 'USER_INFO'
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    email: Mapped[str] = mapped_column(String(30), nullable=True)
    password: Mapped[str] = mapped_column(String(30), nullable=True)

class Post(db.Model):
    __tablename__ = 'POST'
    post_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    user_id: Mapped[int] = mapped_column(String(30), nullable=True)
    title: Mapped[str] = mapped_column(String(30), nullable=True)
    content: Mapped[str] = mapped_column(String(30), nullable=True)
    tag: Mapped[str] = mapped_column(String(30), nullable=True)
    time: Mapped[str] = mapped_column(String(30), nullable=True)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        user = User.query.filter_by(user_id=user_id).first()
        if user:
            flash('user_id已經存在 請重新輸入','user_id')
            return redirect(url_for('register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('email已經存在，請重新輸入')
            return redirect(url_for('register', 'email'))

        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[!@#$%^&*()]", password):
            flash('密碼必須大於8個字且包含至少一個大寫字母，至少一個小寫字母，至少一個特殊字元','password')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('密碼不相同', 'confirm_password')
            return redirect(url_for('register'))

        new_user = User(user_id=user_id, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('註冊成功')
        return redirect(url_for('register'))
    else:
        return render_template('auth/register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            flash('帳號不存在')
            return redirect(url_for('login'))
        if user.password != password:
            flash('密碼錯誤')
            return redirect(url_for('login'))
        session['user_id'] = user.user_id
        return redirect(url_for('index'))
    return render_template('auth/login.html')

@app.route('/index')
def index():
    users = User.query.all()  # get all rows from USER_INFO table
    return render_template('index.html', users=users, sayHello='Hello World!')    

@app.route('/home', methods=['POST', 'GET'])
def home():
    posts=Post.query.all()
    return render_template('HomePage.html',posts=posts)

@app.route('/article', methods=['POST', 'GET'])
def article():
    return render_template('ArticlePage.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('AboutPage.html')