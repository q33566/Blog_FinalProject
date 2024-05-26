from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.post import Post, Comment
import datetime
from personalBlog.db import db
from flask_login import current_user

def homeDef(style):
    if style is None:
        style = 'recommanded_view'
    if style == 'recommanded_view':
        posts = Post.query.all()
        return render_template('post/HomePage.html',posts=posts,style=style)
    if style == 'new_view':
        posts = Post.query.order_by(Post.time.desc()).all()
        return render_template('post/HomePage.html',posts=posts,style=style)
    if style == 'hot_view':
        posts = Post.query.order_by(Post.view_count.desc()).all()
        return render_template('post/HomePage.html',posts=posts,style=style)
    posts=Post.query.all()
    return render_template('post/HomePage.html',posts=posts,style=style)


def articleDef():
    if request.method == 'POST':
        title = request.form['title']  
        tag = request.form['tag']
        intro = request.form['intro']
        content = request.form['content']
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_count = 0
        new_post = Post(title=title, tag=tag, intro=intro, content=content, time=time, view_count=view_count)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.home',style='recommanded_view'))
    return render_template('post/ArticlePage.html')

def editDef():
    if request.method == 'POST':
        posts=Post.query.all()
        return render_template('post/EditPage.html',posts=posts)
    posts=Post.query.all()
    return render_template('post/EditPage.html',posts=posts)


def editarticleDef(id):
    if request.method == 'POST':
        post_id = request.form['post_id']
        db.session.query(Post).filter(Post.post_id == post_id).delete()
        title = request.form['title']  
        tag = request.form['tag']
        intro = request.form['intro']
        content = request.form['content']
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_count = 0
        new_post = Post(post_id=post_id, title=title, tag=tag, intro=intro, content=content, time=time, view_count=view_count)
        db.session.add(new_post)
        db.session.commit()
        print("edit article success")
        return redirect(url_for('post.home',style='recommanded_view'))
    post = Post.query.filter_by(post_id=id).first()
    return render_template('post/EditArticlePage.html',post=post)


def deletearticleDef(id):
    db.session.query(Post).filter(Post.post_id == id).delete()
    db.session.commit()
    return redirect(url_for('post.home',style='recommanded_view'))

def articleViewDef(id):
    if request.method == 'POST':
        post_id = id
        user_id = current_user.user_id
        comment = request.form['comment']
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment = Comment(post_id=post_id, comment=comment, time=time)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post.articleview', id=post_id))
    post = Post.query.filter_by(post_id=id).first()
    comments = Comment.query.filter_by(post_id=id).all()
    post.view_count += 1
    db.session.commit()
    return render_template('post/ArticleViewPage.html',post=post,comments=comments)

def tagViewDef(tag):
    if request.method == 'POST':
        posts = Post.query.filter(Post.tag.like('%'+tag+'%')).all()
        return render_template('post/HomePage.html',posts=posts,style='tag_view')
    posts = Post.query.filter(Post.tag.like('%'+tag+'%')).all()
    return render_template('post/HomePage.html',posts=posts,style='tag_view')