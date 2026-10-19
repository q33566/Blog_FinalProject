import pytest

from personalBlog import create_app
from personalBlog.config import TestConfig
from personalBlog.extensions import db
from personalBlog.models import Post, User


@pytest.fixture
def app(tmp_path):
    app = create_app(TestConfig)
    app.static_folder = str(tmp_path)  # 上傳的圖片寫到暫存資料夾
    (tmp_path / 'uploads').mkdir()
    with app.app_context():
        admin = User(user_id='coffee', email='admin@example.com', is_admin=True)
        admin.set_password('admin-pass!')
        reader = User(user_id='reader', email='reader@example.com')
        reader.set_password('reader-pass!')
        db.session.add_all([admin, reader])
        db.session.commit()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, user_id, password):
    return client.post('/auth/login', data={'user_id': user_id, 'password': password})


@pytest.fixture
def admin_client(client):
    login(client, 'coffee', 'admin-pass!')
    return client


@pytest.fixture
def reader_client(client):
    login(client, 'reader', 'reader-pass!')
    return client


@pytest.fixture
def post(app):
    post = Post(title='Hello', tags='python,flask', intro='intro', content='body')
    db.session.add(post)
    db.session.commit()
    return post
