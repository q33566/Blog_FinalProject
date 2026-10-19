from flask_login import AnonymousUserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()


class AnonymousUser(AnonymousUserMixin):
    is_admin = False


login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'auth.login'
login_manager.login_message = '請先登入'
