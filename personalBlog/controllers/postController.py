from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.post import Post
import datetime
from personalBlog.db import db


def homeDef():
    if request.method == 'POST':
        posts=Post.query.all()
        return render_template('post/HomePage.html',posts=posts)
    posts=Post.query.all()
    return render_template('post/HomePage.html',posts=posts)


def articleDef():
    if request.method == 'POST':
        title = request.form['title']  
        tag = request.form['tag']
        intro = request.form['intro']
        content = request.form['content']
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_post = Post(title=title, tag=tag, intro=intro, content=content, time=time)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.home'))
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
        new_post = Post(post_id=post_id, title=title, tag=tag, intro=intro, content=content, time=time)
        db.session.add(new_post)
        db.session.commit()
        print("edit article success")
        return redirect(url_for('post.home'))
    post = Post.query.filter_by(post_id=id).first()
    return render_template('post/EditArticlePage.html',post=post)


def deletearticleDef(id):
    db.session.query(Post).filter(Post.post_id == id).delete()
    db.session.commit()
    return redirect(url_for('post.home'))

def articleViewDef(id):
    post = Post.query.filter_by(post_id=id).first()
    return render_template('post/ArticleViewPage.html',post=post)