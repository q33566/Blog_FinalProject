from datetime import datetime
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from personalBlog.extensions import db


def normalize_tags(raw):
    """'a, b,,a ' -> 'a,b'：去空白、去空字串、去重複並保留順序。"""
    tags = [t.strip() for t in raw.split(',')]
    return ','.join(dict.fromkeys(t for t in tags if t))


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    tags: Mapped[str] = mapped_column(String(200))
    intro: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    view_count: Mapped[int] = mapped_column(default=0)

    comments: Mapped[list['Comment']] = relationship(
        back_populates='post', cascade='all, delete-orphan', order_by='Comment.created_at')

    @property
    def tag_list(self):
        return self.tags.split(',') if self.tags else []


class Comment(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    post: Mapped['Post'] = relationship(back_populates='comments')
