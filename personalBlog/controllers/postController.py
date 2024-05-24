from flask import redirect,url_for,render_template,request,session,flash, Blueprint
from personalBlog.models.post import Post
import datetime
from personalBlog.db import db


def homeDef():
    #posts=Post.query.all()
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