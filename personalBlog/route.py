from flask import Blueprint
from personalBlog.controllers.authController import  registerDef, loginDef

auth = Blueprint('auth', __name__, template_folder='templates/auth')

@auth.route('/register', methods=['POST', 'GET'])
def register():
    return registerDef()

@auth.route('/login', methods=['POST','GET'])
def login():
    return loginDef()