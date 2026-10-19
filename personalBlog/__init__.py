import os
from datetime import datetime

import click
from flask import Flask, render_template

from personalBlog.config import Config
from personalBlog.extensions import csrf, db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, app.config['UPLOAD_SUBDIR']), exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from personalBlog.views.about import bp as about_bp
    from personalBlog.views.auth import bp as auth_bp
    from personalBlog.views.post import bp as post_bp
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(about_bp, url_prefix='/about')

    from personalBlog.rendering import render_markdown, zh_date
    app.jinja_env.filters['markdown'] = render_markdown
    app.jinja_env.filters['zh_date'] = zh_date

    @app.context_processor
    def inject_author():
        # 頁尾和首頁刊頭都會用到作者資料
        from personalBlog.models import About
        return {'author': db.session.scalar(db.select(About)), 'now': datetime.now()}

    register_error_handlers(app)
    register_commands(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    messages = {403: '你沒有權限查看這個頁面', 404: '找不到這個頁面', 413: '圖片太大，請小於 16 MB'}

    def handle(error):
        return render_template('error.html', code=error.code, message=messages[error.code]), error.code

    for code in messages:
        app.register_error_handler(code, handle)


def register_commands(app):
    from personalBlog.demo import seed_demo
    from personalBlog.models import User

    app.cli.add_command(seed_demo)

    @app.cli.command('create-admin')
    @click.option('--user-id', prompt=True)
    @click.option('--email', prompt=True)
    @click.password_option()
    def create_admin(user_id, email, password):
        """建立（或將既有帳號升級為）管理員。"""
        user = db.session.get(User, user_id)
        if user is None:
            user = User(user_id=user_id, email=email)
            db.session.add(user)
        user.set_password(password)
        user.is_admin = True
        db.session.commit()
        click.echo(f'管理員 {user_id} 已建立')
