from datetime import datetime, timedelta

import click
from flask.cli import with_appcontext

from personalBlog.extensions import db
from personalBlog.models import About, Comment, Post, User

DEMO_PASSWORD = 'demo-pass!'
ADMIN_ID = 'linyan'
READERS = ['mia_chen', '阿哲', 'tsai.dev']

# (天數前, 標題, tags, 簡介, 瀏覽數, 內文)
POSTS = [
    (152, 'Git rebase 前我會先做的三件事', 'git',
     '每次 rebase 出事，都是因為少做了其中一步。', 318, '''\
rebase 很好用，但改壞了很難救。這是我現在的固定流程。

## 1. 先看清楚要搬哪些 commit

```bash
git fetch origin
git log --oneline origin/main..HEAD
```

列出來的就是這次會被重新套用的 commit。數量比預期多，通常代表分支切錯了。

## 2. 留一個備份分支

```bash
git branch backup/payment-refactor
```

就算 `git reflog` 也救得回來，有一個名字清楚的分支還是安心很多。確定沒問題再刪掉。

## 3. 推送用 `--force-with-lease`

```bash
git push --force-with-lease
```

如果遠端在你 rebase 的時候被別人推了新 commit，`--force-with-lease` 會拒絕覆蓋，`--force` 不會。
'''),
    (118, '讀《資料密集型應用系統設計》第一章', '讀書,database',
     '可靠、可擴展、可維護：三個詞聽起來很空，書裡講得很具體。', 204, '''\
這本書很多人推薦，終於從第一章開始認真讀。

## 用百分位數描述回應時間

平均值會掩蓋問題。書裡建議看 p50、p95、p99：

| 指標 | 意思 |
| --- | --- |
| p50 | 一半的請求比這個快 |
| p99 | 只有 1% 的請求比這個慢 |

最慢的那 1% 往往是資料最多的使用者，也常是最重要的客戶。

## 先描述負載，再談擴展

作者用 Twitter 的首頁時間軸當例子：是在讀取時才合併關注對象的推文，還是在發文時就寫進每個追蹤者的時間軸？哪一種比較好，取決於讀寫比例，以及有沒有追蹤者特別多的帳號。

> 擴展性不是「這個系統能不能擴展」，而是「負載用這種方式成長時，我們有什麼選擇」。

下一章是資料模型，讀完再整理。
'''),
    (87, 'Docker 容器裡的時間為什麼差 8 小時', 'docker,linux',
     '本機跑得好好的排程，進了容器就提早 8 小時觸發。', 587, '''\
上線後發現每天早上 9 點的排程，在凌晨 1 點就跑了。

## 原因

容器預設時區是 UTC，台灣是 UTC+8。程式裡用 `datetime.now()` 拿到的是容器的當地時間，也就是 UTC。

```bash
docker run --rm python:3.12-slim date
```

## 解法

在 Dockerfile 設定 `TZ`。有些精簡映像檔沒有時區資料，要另外安裝 `tzdata`：

```dockerfile
FROM python:3.12-slim
ENV TZ=Asia/Taipei
RUN apt-get update \\
 && apt-get install -y --no-install-recommends tzdata \\
 && rm -rf /var/lib/apt/lists/*
```

不過這只是讓排程對上。資料庫裡的時間我後來全部改存 UTC，只在顯示時才轉成台灣時間，下一篇再寫。
'''),
    (80, 'Python datetime 的 naive 與 aware', 'python',
     '上一篇的後續：為什麼我決定一律使用帶時區的時間。', 241, '''\
Python 的 `datetime` 分兩種：

- **naive**：沒有時區資訊，例如 `datetime.now()`
- **aware**：帶有時區，例如 `datetime.now(timezone.utc)`

兩種混在一起比較會直接報錯：

```python
>>> datetime.now() < datetime.now(timezone.utc)
TypeError: can't compare offset-naive and offset-aware datetimes
```

## 我現在的做法

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

created_at = datetime.now(timezone.utc)                     # 存進資料庫
shown = created_at.astimezone(ZoneInfo('Asia/Taipei'))      # 顯示給使用者
```

另外，`datetime.utcnow()` 在 Python 3.12 已經被標為 deprecated，因為它回傳的是 naive 時間，很容易被誤當成當地時間。
'''),
    (41, '用 EXPLAIN ANALYZE 找出慢查詢', 'postgresql,database',
     '訂單列表頁越來越慢，最後只加了一個索引。', 129, '''\
訂單列表頁的回應時間從 200ms 慢慢爬到 2 秒多。

## 先看查詢計畫

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 42
ORDER BY created_at DESC
LIMIT 20;
```

結果裡出現 `Seq Scan on orders`：整張表從頭掃到尾，再排序取前 20 筆。

## 加上複合索引

```sql
CREATE INDEX CONCURRENTLY idx_orders_user_created
    ON orders (user_id, created_at DESC);
```

再跑一次，變成 `Index Scan using idx_orders_user_created`，執行時間回到幾毫秒。

幾個提醒：

- `EXPLAIN ANALYZE` 會**真的執行**查詢，對 `UPDATE`、`DELETE` 要包在交易裡再 rollback
- 線上環境建索引記得加 `CONCURRENTLY`，不然會鎖住寫入
'''),
    (9, '給自己的 code review 清單', '工作',
     '幫別人 review 時，我會依序問自己這幾個問題。', 46, '''\
review 久了發現，自己最常漏看的總是同幾類問題，乾脆寫成清單。

1. **這個 PR 在解決什麼問題？** 看不出來就先問，不要急著看程式碼。
2. **錯誤情況怎麼處理？** 網路失敗、資料是空的、使用者沒有權限。
3. **有沒有測試會在改壞時失敗？** 有測試不代表有測到重點。
4. **命名讀得懂嗎？** 需要靠註解才看得懂的名字，通常可以再改。
5. **要不要現在改？** 不是每個意見都要擋 PR，可以標成之後再處理。

最後一點最難。我現在會在意見前面加上「必改」或「建議」，讓對方知道輕重。
'''),
]

# (文章索引, 留言者, 發文後幾天又幾小時, 內容)
COMMENTS = [
    (0, 'tsai.dev', 3.2, '第二點很實用，之前 rebase 壞掉都是靠 reflog 慢慢翻。'),
    (1, 'mia_chen', 5.6, 'p99 那段很有感，我們的監控之前只看平均，難怪一直抓不到問題。'),
    (2, '阿哲', 0.4, '我們也遇過一樣的事！不過我們是在 docker-compose 裡掛 /etc/localtime。'),
    (2, ADMIN_ID, 0.9, '掛 /etc/localtime 也可以，但會跟主機綁在一起，換機器時要注意主機的時區設定。'),
    (2, 'mia_chen', 6.3, '想問存 UTC 之後，報表要按「台灣的日期」分組要怎麼寫？'),
    (2, ADMIN_ID, 7.1, '在 SQL 裡先轉時區再取日期，PostgreSQL 可以用 created_at AT TIME ZONE \'Asia/Taipei\'。'),
    (4, 'tsai.dev', 2.8, '提醒一下，CONCURRENTLY 不能在交易裡執行，用 migration 工具時要特別設定。'),
]


@click.command('seed-demo')
@with_appcontext
def seed_demo():
    """建立示範用的帳號、文章與留言（內容皆為虛構）。"""
    if db.session.scalar(db.select(Post)):
        click.echo('資料庫已經有文章，略過')
        return

    users = [User(user_id=ADMIN_ID, email='linyan@example.com', is_admin=True)]
    users += [User(user_id=name, email=f'reader{i}@example.com') for i, name in enumerate(READERS)]
    for user in users:
        user.set_password(DEMO_PASSWORD)
    db.session.add_all(users)

    now = datetime.now()
    posts = []
    for days_ago, title, tags, intro, views, content in POSTS:
        created = (now - timedelta(days=days_ago)).replace(hour=21, minute=days_ago % 60)
        posts.append(Post(title=title, tags=tags, intro=intro, content=content,
                          view_count=views, created_at=created, updated_at=created))
    db.session.add_all(posts)

    for index, user_id, after_days, content in COMMENTS:
        post = posts[index]
        db.session.add(Comment(post=post, user_id=user_id, content=content,
                               created_at=post.created_at + timedelta(days=after_days)))

    db.session.add(About(name='林言', email='linyan@example.com',
                         introduction='後端工程師，平常寫 Python 和 SQL。\n'
                                      '這裡記錄工作上踩過的坑和讀書筆記。'))
    db.session.commit()
    click.echo(f'示範資料已建立：管理員 {ADMIN_ID}，一般會員 {"、".join(READERS)}，密碼都是 {DEMO_PASSWORD}')
