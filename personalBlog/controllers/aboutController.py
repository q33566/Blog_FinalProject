from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.user import User
from personalBlog.models.about import About
from personalBlog.db import db
from flask_login import current_user
from personalBlog.form import AboutForm
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
def aboutDef():
    about = About.query.first()
    if about is None:
        return render_template('about/about.html', image_url = '/uploads/default.jpg', introduction = '部落格擁有者沒有提供個人訊息', name = '無', email = 'no email')
    return render_template('about/about.html', image_url = '/uploads/'+about.filename , introduction = about.introduction, name = about.name, email = about.email)

def editAboutGetDef():
    about = About.query.first()
    form = AboutForm()
    if about is not None:
        form.name.data = about.name
        form.about_me.data = about.introduction
        form.email.data = about.email
    if current_user.user_id != "coffee":
        redirect(url_for('about.about'))
    return render_template('about/editAbout.html', form = form)

def editAboutPostDef():
    if current_user.user_id != "coffee":
        redirect(url_for('about.about'))
    form = AboutForm()
    about = About.query.first()
    if form.validate_on_submit():
        name = form.name.data
        introduction = form.about_me.data
        email = form.email.data
        if form.picture.data:
            filename = secure_filename(form.picture.data.filename)
        # Check if a file was uploaded
        if form.picture.data:
            # Save the picture
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            for filename in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, filename))
            form.picture.data.save(os.path.join( UPLOAD_FOLDER, filename))
            # Update the user's picture
        # Save the changes to the database
        if about is None:
            # The About table is empty, so create a new row
            about = About(name = name, introduction = introduction, filename = filename, email = email)
            db.session.add(about)
            db.session.commit()
        else:
            # The About table is not empty, so update the existing row
            about.name = name
            about.introduction = introduction
            if form.picture.data:
                about.filename = filename
            about.email = email
            db.session.commit()
        db.session.commit()

        flash('自我介紹頁面更新成功', 'success')
        return redirect(url_for('about.about', image_url = '/uploads/'+about.filename, introduction = about.introduction, name = about.name, email = about.email))
    return render_template('about/editAbout.html', form = form)
