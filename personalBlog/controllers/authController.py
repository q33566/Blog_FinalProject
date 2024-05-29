from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.user import User
import re
from personalBlog.db import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from personalBlog.form import RegistrationForm, LoginForm

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)      

def logoutDef():
    logout_user()
    return redirect(url_for('auth.login'))

def registerDef():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(user_id=form.user_id.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('註冊成功','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

def loginDef():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        user = User.query.get(user_id)
        if user is None:
            flash('ID不存在或密碼錯誤','ID_does_not_exist')
            return redirect(url_for('auth.login'))
        elif not user.check_password(password):  # assuming your User model has a check_password method
            flash('ID不存在或密碼錯誤','wrong_password')
            return redirect(url_for('auth.login'))

        login_user(user)

        flash('登入成功','login_success')
        return redirect(url_for('post.home',style='recommanded_view'))  # redirect to the index page after successful login
        
    return render_template('auth/login.html', form = form)  # render the login formfrom flask import request, flash, session