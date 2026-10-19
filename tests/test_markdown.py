from personalBlog.extensions import db
from personalBlog.models import Post


def make_post(content):
    post = Post(title='T', tags='x', intro='i', content=content)
    db.session.add(post)
    db.session.commit()
    return post


def test_article_renders_markdown(client):
    post = make_post('## 小標\n\n```python\nprint("hi")\n```')
    html = client.get(f'/posts/{post.id}').get_data(as_text=True)
    assert '<h2>小標</h2>' in html
    assert '<code class="language-python">' in html


def test_article_strips_dangerous_html(client):
    post = make_post('hello <script>alert(1)</script> <a href="javascript:alert(1)">x</a>')
    html = client.get(f'/posts/{post.id}').get_data(as_text=True)
    assert '<script>alert(1)</script>' not in html
    assert 'javascript:alert' not in html
