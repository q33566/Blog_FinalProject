from flask import Blueprint
from personalBlog.controllers.authController import  registerDef, loginDef, logoutDef
from personalBlog.controllers.postController import homeDef, articleDef
from flask_login import login_required, logout_user
auth = Blueprint('auth', __name__, template_folder='templates/auth')
post = Blueprint('post', __name__, template_folder='templates/post')

@auth.route('/register', methods=['POST', 'GET'])
def register():
    return registerDef()

@auth.route('/login', methods=['POST','GET'])
def login():
    return loginDef()

@auth.route('/logout')
@login_required
def logout():
    return logoutDef()
    
@post.route('/home', methods=['POST', 'GET'])
def home():
    return homeDef()

@post.route('/article', methods=['POST', 'GET'])
def article():
    return articleDef()

