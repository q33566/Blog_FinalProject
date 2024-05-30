from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from personalBlog.db import db

class About(db.Model):
    __tablename__ = 'ABOUT'
    name: Mapped[str] = mapped_column(nullable=False, autoincrement=True)
    introduction: Mapped[str] = mapped_column(String(30), nullable=False)
    filename : Mapped[str] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), nullable=False)