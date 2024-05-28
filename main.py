from flask import Flask,redirect,url_for,render_template,request,session,flash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = '/personalBlog/static/image'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def home():
    return redirect(url_for('post.home',style='recommanded_view'))

from personalBlog.route import auth
app.register_blueprint(auth, url_prefix='/auth')

from personalBlog.route import post
app.register_blueprint(post, url_prefix='/post')

from personalBlog.route import aboutBp
app.register_blueprint(aboutBp, url_prefix='')

from personalBlog import db
db.init_db(app)

from personalBlog.controllers.authController import login_manager
login_manager.init_app(app)







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