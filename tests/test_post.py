import pytest

from personalBlog.extensions import db
from personalBlog.models import Comment, Post
from personalBlog.models.post import normalize_tags

ARTICLE = {'title': 'New', 'tags': ' a, b ,,a', 'intro': 'short', 'content': 'long'}


def test_normalize_tags():
    assert normalize_tags(' a, b ,,a') == 'a,b'


@pytest.mark.parametrize('sort', ['latest', 'popular', 'bogus'])
def test_home_sorts(client, post, sort):
    resp = client.get(f'/?sort={sort}')
    assert resp.status_code == 200
    assert 'Hello' in resp.get_data(as_text=True)


def test_detail_counts_views(client, post):
    client.get(f'/posts/{post.id}')
    client.get(f'/posts/{post.id}')
    assert db.session.get(Post, post.id).view_count == 2


def test_missing_post_is_404(client):
    assert client.get('/posts/999').status_code == 404


@pytest.mark.parametrize('method, url', [
    ('get', '/posts/new'), ('post', '/posts/new'), ('get', '/posts/manage'),
    ('get', '/posts/{id}/edit'), ('post', '/posts/{id}/delete'),
])
def test_reader_cannot_use_admin_pages(reader_client, post, method, url):
    resp = getattr(reader_client, method)(url.format(id=post.id), data=ARTICLE)
    assert resp.status_code == 403


def test_anonymous_is_redirected_to_login(client):
    resp = client.get('/posts/new')
    assert resp.status_code == 302
    assert '/auth/login' in resp.location


def test_admin_creates_post(admin_client):
    resp = admin_client.post('/posts/new', data=ARTICLE)
    assert resp.status_code == 302
    post = db.session.scalar(db.select(Post).filter_by(title='New'))
    assert post.tags == 'a,b'


def test_admin_edit_keeps_id_and_views(admin_client, post):
    post.view_count = 7
    db.session.commit()
    admin_client.post(f'/posts/{post.id}/edit', data=ARTICLE)
    edited = db.session.get(Post, post.id)
    assert edited.title == 'New'
    assert edited.view_count == 7


def test_admin_delete_cascades_comments(admin_client, post):
    db.session.add(Comment(post=post, user_id='reader', content='hi'))
    db.session.commit()
    assert admin_client.post(f'/posts/{post.id}/delete').status_code == 302
    assert db.session.scalar(db.select(db.func.count(Comment.id))) == 0
    assert db.session.get(Post, post.id) is None


def test_delete_requires_post_method(admin_client, post):
    assert admin_client.get(f'/posts/{post.id}/delete').status_code == 405


def test_comment_requires_login(client, post):
    resp = client.post(f'/posts/{post.id}/comments', data={'content': 'hi'})
    assert resp.status_code == 302
    assert db.session.scalar(db.select(db.func.count(Comment.id))) == 0


def test_reader_comments(reader_client, post):
    reader_client.post(f'/posts/{post.id}/comments', data={'content': 'nice post'})
    html = reader_client.get(f'/posts/{post.id}').get_data(as_text=True)
    assert 'nice post' in html


def test_tag_filter_is_exact(client, post):
    db.session.add(Post(title='Py only', tags='py', intro='i', content='c'))
    db.session.commit()
    html = client.get('/tags/py').get_data(as_text=True)
    assert 'Py only' in html
    assert 'Hello' not in html  # "python" 不應該被 "py" 命中
    assert client.get('/tags/nothing').status_code == 404


def test_tag_list(client, post):
    html = client.get('/tags').get_data(as_text=True)
    assert 'python' in html and 'flask' in html
