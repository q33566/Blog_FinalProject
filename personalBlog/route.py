from flask import Blueprint
from flask_login import login_required, logout_user
from personalBlog.controllers.authController import  registerDef, loginDef, logoutDef
from personalBlog.controllers.postController import homeDef, articleDef, editDef, editarticleDef, deletearticleDef, articleViewDef, tagViewDef, tagListDef
from personalBlog.controllers.aboutController import aboutDef, editAboutGetDef, editAboutPostDef
auth = Blueprint('auth', __name__, template_folder='templates/auth')
post = Blueprint('post', __name__, template_folder='templates/post')
aboutBp = Blueprint('about', __name__, template_folder='templates/about')

@aboutBp.route('/about', methods=['GET'])
def about():
    return aboutDef()

@aboutBp.route('/editAbout', methods=['GET'])
def editAboutGet():
    return editAboutGetDef()

@aboutBp.route('/editAbout', methods=['POST'])
def editAboutPost():
    return editAboutPostDef()

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
    
@post.route('/home/<string:style>', methods=['POST', 'GET'])
def home(style):
    return homeDef(style)

@post.route('/article', methods=['POST', 'GET'])
def article():
    return articleDef()

@post.route('/edit', methods=['POST', 'GET'])
def edit():
    return editDef()

@post.route('/editarticle/<int:id>', methods=['POST', 'GET'])
def editarticle(id):
    return editarticleDef(id)

@post.route('/deletearticle/<int:id>', methods=['POST', 'GET'])
def deletearticle(id):
    return deletearticleDef(id)

@post.route('/articleview/<int:id>', methods=['POST', 'GET'])
def articleview(id):
    return articleViewDef(id)

@post.route('/taglist', methods=['POST', 'GET'])
def tag():
    return tagListDef()

@post.route('/tagview/<string:tag>', methods=['POST', 'GET'])
def tagview(tag):
    return tagViewDef(tag)