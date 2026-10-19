from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from personalBlog.extensions import db


class About(db.Model):
    """「關於我」頁面，整個部落格只會有一筆資料。"""
    __tablename__ = 'about'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    introduction: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(120))
    image_filename: Mapped[str | None] = mapped_column(String(100))
