import os
import uuid

from flask import Blueprint, current_app, flash, redirect, render_template, url_for

from personalBlog.decorators import admin_required
from personalBlog.extensions import db
from personalBlog.forms import AboutForm
from personalBlog.models import About

bp = Blueprint('about', __name__)


@bp.route('')
def show():
    about = db.session.scalar(db.select(About))
    return render_template('about/show.html', about=about)


@bp.route('/edit', methods=['GET', 'POST'])
@admin_required
def edit():
    about = db.session.scalar(db.select(About))
    form = AboutForm()
    if form.validate_on_submit():
        if about is None:
            about = About()
            db.session.add(about)
        about.name = form.name.data
        about.introduction = form.about_me.data
        about.email = form.email.data
        if form.picture.data:
            old_filename = about.image_filename
            about.image_filename = _save_picture(form.picture.data)
            _remove_picture(old_filename)
        db.session.commit()
        flash('已儲存關於我')
        return redirect(url_for('about.show'))
    if about is not None and not form.is_submitted():
        form.name.data = about.name
        form.about_me.data = about.introduction
        form.email.data = about.email
    return render_template('about/edit.html', form=form)


def _upload_dir():
    return os.path.join(current_app.static_folder, current_app.config['UPLOAD_SUBDIR'])


def _save_picture(file):
    # 用隨機檔名存檔，避免檔名衝突與瀏覽器快取到舊圖
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f'{uuid.uuid4().hex}{ext}'
    file.save(os.path.join(_upload_dir(), filename))
    return filename


def _remove_picture(filename):
    if filename:
        path = os.path.join(_upload_dir(), filename)
        if os.path.exists(path):
            os.remove(path)
