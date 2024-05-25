from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from personalBlog.db import db

class Post(db.Model):
    __tablename__ = 'POST'
    post_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    title: Mapped[str] = mapped_column(String(30), nullable=True)
    tag: Mapped[str] = mapped_column(String(30), nullable=True)
    intro: Mapped[str] = mapped_column(String(30), nullable=True)
    content: Mapped[str] = mapped_column(String(30), nullable=True)
    time: Mapped[str] = mapped_column(String(30), nullable=True)