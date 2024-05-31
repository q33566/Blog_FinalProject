from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.post import Post, Comment
from personalBlog.models.user import User
from personalBlog.form import ArticleForm
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
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        tag = form.tag.data
        intro = form.intro.data
        content = form.content.data
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_count = 0
        new_post = Post(title=title, tag=tag, intro=intro, content=content, time=time, view_count=view_count)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.home',style='recommanded_view'))
    return render_template('post/ArticlePage.html', form=form)

def editDef():
    if current_user.user_id != "coffee":
        return redirect(url_for('post.home',style='recommanded_view'))
    if request.method == 'POST':
        posts=Post.query.all()
        return render_template('post/EditPage.html',posts=posts)
    posts=Post.query.all()
    return render_template('post/EditPage.html',posts=posts)


def editarticleDef(id):
    if current_user.user_id != "coffee":
        return redirect(url_for('post.home',style='recommanded_view'))
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
    if current_user.user_id != "coffee":
        return redirect(url_for('post.home',style='recommanded_view'))
    db.session.query(Post).filter(Post.post_id == id).delete()
    db.session.query(Comment).filter(Comment.post_id == id).delete()
    db.session.commit()
    return redirect(url_for('post.home',style='recommanded_view'))

def articleViewDef(id):
    if request.method == 'POST':
        post_id = id
        
        user_id = current_user.user_id
        comment = request.form['comment']
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment = Comment(post_id=post_id, comment=comment, time=time, user_id = user_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('post.articleview', id=post_id))
    post = Post.query.filter_by(post_id=id).first()
    comments = Comment.query.filter_by(post_id=id).all()
    post.view_count += 1
    db.session.commit()
    return render_template('post/ArticleViewPage.html',post=post,comments=comments)

def tagListDef():
    posts = Post.query.all()
    tags = []
    for post in posts:
        tag = post.tag.split(',')
        for t in tag:
            if t not in tags:
                tags.append(t)
    return render_template('post/TagPage.html',tags=tags)

def tagViewDef(tag):
    if request.method == 'POST':
        posts = Post.query.filter(Post.tag.like('%'+tag+'%')).all()
        return render_template('post/HomePage.html',posts=posts,style='tag_view')
    posts = Post.query.filter(Post.tag.like('%'+tag+'%')).all()
    return render_template('post/HomePage.html',posts=posts,style='tag_view')