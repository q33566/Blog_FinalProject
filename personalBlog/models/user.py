from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from personalBlog.db import db


class User(db.Model):
    __tablename__  = 'USER_INFO'
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    email: Mapped[str] = mapped_column(String(30), nullable=True)
    password: Mapped[str] = mapped_column(String(30), nullable=True)