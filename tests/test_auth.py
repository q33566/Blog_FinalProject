from personalBlog.extensions import db
from personalBlog.models import User


def test_register_stores_hashed_password(client):
    resp = client.post('/auth/register', data={
        'user_id': 'alice', 'email': 'alice@example.com',
        'password': 'secret-pass!', 'confirm_password': 'secret-pass!',
    })
    assert resp.status_code == 302
    user = db.session.get(User, 'alice')
    assert user.password_hash != 'secret-pass!'
    assert user.check_password('secret-pass!')
    assert not user.is_admin


def test_register_rejects_duplicate_id_and_weak_password(client):
    resp = client.post('/auth/register', data={
        'user_id': 'reader', 'email': 'new@example.com',
        'password': 'short', 'confirm_password': 'short',
    })
    html = resp.get_data(as_text=True)
    assert '這個帳號已經有人使用' in html
    assert '密碼至少要 8 個字元' in html


def test_login_with_wrong_password_fails(client):
    resp = client.post('/auth/login', data={'user_id': 'reader', 'password': 'nope'},
                       follow_redirects=True)
    assert '帳號或密碼錯誤' in resp.get_data(as_text=True)


def test_login_and_logout(reader_client):
    assert 'href="/auth/logout"' in reader_client.get('/').get_data(as_text=True)
    reader_client.get('/auth/logout')
    assert 'href="/auth/logout"' not in reader_client.get('/').get_data(as_text=True)


def test_create_admin_command(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=['create-admin', '--user-id', 'boss', '--email', 'boss@example.com',
                                 '--password', 'boss-pass!'])
    assert result.exit_code == 0
    assert db.session.get(User, 'boss').is_admin
