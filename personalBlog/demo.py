from datetime import datetime, timedelta

import click
from flask.cli import with_appcontext

from personalBlog.extensions import db
from personalBlog.models import About, Comment, Post, User

POSTS = [
    ('用 Flask Blueprint 拆分專案', 'python,flask',
     '當路由超過十個，把所有東西塞在 app.py 就開始難以維護。',
     '剛開始寫 Flask 時，所有路由都放在同一個檔案裡。\n\n'
     '功能變多之後，我把專案拆成 auth、post、about 三個 Blueprint，'
     '每個 Blueprint 只負責自己的路由與樣板，再由 create_app() 統一註冊。\n\n'
     '這樣做的好處是測試時可以用不同設定建立 app，也更容易找到程式碼。', 42),
    ('密碼不該用明文儲存', 'security,python',
     '從 werkzeug.security 開始，談密碼雜湊的基本觀念。',
     '早期版本把密碼直接存進資料庫，資料庫外流就等於所有帳號外流。\n\n'
     '改用 generate_password_hash 之後，資料庫裡只剩下加鹽的雜湊值，'
     '登入時再用 check_password_hash 比對。', 87),
    ('SQLAlchemy 2.0 的型別標註寫法', 'python,sqlalchemy',
     'Mapped[] 與 mapped_column() 讓 model 定義更清楚。',
     'SQLAlchemy 2.0 推薦用 Mapped[int] 這類型別標註宣告欄位，\n'
     'nullable 會從型別自動推導，編輯器也能正確提示。', 23),
    ('為什麼刪除要用 POST', 'security,web',
     'GET 請求應該是安全的，刪除資料卻用連結觸發會出事。',
     '瀏覽器預先載入、爬蟲或是別人貼給你的連結，都可能在你不知情的狀況下送出 GET 請求。\n\n'
     '把刪除改成 POST 並加上 CSRF token，就能確保這個動作是使用者自己按下的。', 15),
]


@click.command('seed-demo')
@with_appcontext
def seed_demo():
    """建立示範用的帳號、文章與留言。"""
    if db.session.scalar(db.select(Post)):
        click.echo('資料庫已經有文章，略過')
        return
    admin = db.session.get(User, 'admin') or User(user_id='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin-pass!')
    reader = db.session.get(User, 'reader') or User(user_id='reader', email='reader@example.com')
    reader.set_password('reader-pass!')
    db.session.add_all([admin, reader])

    now = datetime.now()
    for i, (title, tags, intro, content, views) in enumerate(POSTS):
        created = now - timedelta(days=(len(POSTS) - i) * 9)
        db.session.add(Post(title=title, tags=tags, intro=intro, content=content,
                            view_count=views, created_at=created, updated_at=created))
    db.session.flush()

    first = db.session.scalar(db.select(Post).order_by(Post.id))
    db.session.add_all([
        Comment(post=first, user_id='reader', content='拆完之後測試真的好寫很多！'),
        Comment(post=first, user_id='admin', content='對，create_app 是關鍵。'),
    ])
    if db.session.scalar(db.select(About)) is None:
        db.session.add(About(name='部落格作者', email='admin@example.com',
                             introduction='喜歡寫後端與整理筆記的工程師。\n這裡記錄我學 Python 與 Web 開發的過程。'))
    db.session.commit()
    click.echo('示範資料已建立：admin / admin-pass!、reader / reader-pass!')
