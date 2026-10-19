from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import selectinload

from personalBlog.decorators import admin_required
from personalBlog.extensions import db
from personalBlog.forms import ArticleForm, CommentForm
from personalBlog.models import Comment, Post
from personalBlog.models.post import normalize_tags

bp = Blueprint('post', __name__)

# 首頁三種排序：推薦（發文順序）、最新、熱門（瀏覽數）
SORTS = {
    'recommended': Post.id.asc(),
    'latest': Post.created_at.desc(),
    'popular': Post.view_count.desc(),
}


@bp.route('/')
def home():
    sort = request.args.get('sort', 'recommended')
    if sort not in SORTS:
        sort = 'recommended'
    posts = db.session.scalars(
        db.select(Post).options(selectinload(Post.comments)).order_by(SORTS[sort])).all()
    return render_template('post/list.html', posts=posts, sort=sort)


@bp.route('/posts/<int:post_id>')
def detail(post_id):
    post = db.get_or_404(Post, post_id)
    post.view_count += 1
    db.session.commit()
    return render_template('post/detail.html', post=post, form=CommentForm())


@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def add_comment(post_id):
    post = db.get_or_404(Post, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(post=post, user_id=current_user.user_id, content=form.content.data))
        db.session.commit()
    return redirect(url_for('post.detail', post_id=post.id))


@bp.route('/posts/new', methods=['GET', 'POST'])
@admin_required
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        post = Post()
        _fill_post(post, form)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.detail', post_id=post.id))
    return render_template('post/form.html', form=form, heading='寫文章', submit_label='發布')


@bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(post_id):
    post = db.get_or_404(Post, post_id)
    form = ArticleForm(obj=post)
    if form.validate_on_submit():
        _fill_post(post, form)
        db.session.commit()
        return redirect(url_for('post.detail', post_id=post.id))
    return render_template('post/form.html', form=form, heading='編輯文章', submit_label='儲存變更')


@bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@admin_required
def delete(post_id):
    db.session.delete(db.get_or_404(Post, post_id))
    db.session.commit()
    return redirect(url_for('post.manage'))


@bp.route('/posts/manage')
@admin_required
def manage():
    posts = db.session.scalars(db.select(Post).order_by(Post.id)).all()
    return render_template('post/manage.html', posts=posts)


@bp.route('/tags')
def tags():
    posts = db.session.scalars(db.select(Post).order_by(Post.id)).all()
    all_tags = dict.fromkeys(tag for post in posts for tag in post.tag_list)
    return render_template('post/tags.html', tags=list(all_tags))


@bp.route('/tags/<tag>')
def by_tag(tag):
    # 標籤以逗號字串儲存，用 LIKE 粗篩後再做精確比對，避免 "py" 命中 "python"
    candidates = db.session.scalars(db.select(Post).where(Post.tags.contains(tag)).order_by(Post.id))
    posts = [post for post in candidates if tag in post.tag_list]
    if not posts:
        abort(404)
    return render_template('post/list.html', posts=posts, sort=None, tag=tag)


def _fill_post(post, form):
    post.title = form.title.data
    post.tags = normalize_tags(form.tags.data)
    post.intro = form.intro.data
    post.content = form.content.data
