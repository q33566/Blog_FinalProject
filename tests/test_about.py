import io

from personalBlog.extensions import db
from personalBlog.models import About

FORM = {'name': 'Kurt', 'about_me': 'hi there', 'email': 'kurt@example.com'}


def test_empty_about_page(client):
    assert '部落格擁有者沒有提供個人訊息' in client.get('/about').get_data(as_text=True)


def test_reader_cannot_edit_about(reader_client):
    assert reader_client.post('/about/edit', data=FORM).status_code == 403


def test_admin_creates_about_without_picture(admin_client):
    assert admin_client.post('/about/edit', data=FORM).status_code == 302
    about = db.session.scalar(db.select(About))
    assert about.name == 'Kurt'
    assert about.image_filename is None


def test_admin_edit_form_is_prefilled(admin_client):
    admin_client.post('/about/edit', data=FORM)
    assert 'kurt@example.com' in admin_client.get('/about/edit').get_data(as_text=True)


def test_new_picture_replaces_old_one(app, admin_client, tmp_path):
    def upload():
        data = dict(FORM, picture=(io.BytesIO(b'img'), 'me.png'))
        admin_client.post('/about/edit', data=data, content_type='multipart/form-data')
        return db.session.scalar(db.select(About)).image_filename

    first = upload()
    second = upload()
    assert first != second and second.endswith('.png')
    assert sorted(p.name for p in (tmp_path / 'uploads').iterdir()) == [second]
