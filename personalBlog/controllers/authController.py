from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.user import User
import re
from personalBlog.db import db

def registerDef():
    hasError = False
    if request.method == 'POST':
        user_id = request.form['user_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if user_id == '': 
            flash('user_id不能為空','user_id')
            hasError = True
        else:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                flash('user_id已經存在 請重新輸入','user_id')
                hasError = True
        if email == '':
            flash('email不能為空','email')
            hasError = True
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('email已經存在，請重新輸入','email')
                hasError = True
            elif re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) is None:
                flash('email格式不符','email')
                hasError = True
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[!@#$%^&*()]", password):
            flash('密碼必須大於8個字且包含至少一個大寫字母，至少一個小寫字母，至少一個特殊字元','password')
            hasError = True
        if password != confirm_password:
            flash('密碼不相同', 'confirm_password')
            hasError = True
        
        if(hasError):
            return redirect(url_for('auth.register'))
        else:
            new_user = User(user_id=user_id, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('註冊成功','success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')
    
def loginDef():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        user = User.query.get(user_id)
        if user is None:
            flash('ID不存在','ID_does_not_exist')
            return redirect(url_for('auth.login'))

        if not user.check_password(password):  # assuming your User model has a check_password method
            flash('密碼錯誤','wrong_password')
            return redirect(url_for('auth.login'))

        session['user_id'] = user_id  # store user_id in session
        flash('登入成功','login_success')
        return redirect(url_for('index'))  # redirect to the index page after successful login

    return render_template('auth/login.html')  # render the login formfrom flask import request, flash, session