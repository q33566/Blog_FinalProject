from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from personalBlog.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__  = 'USER_INFO'
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    
    def __init__(self, user_id, email, password):
        """初始化"""
        self.user_id = user_id
        self.email = email
        self.password = password
    def get_id(self):
        return str(self.user_id)
    
    def check_password(self, password):
        """檢查輸入是否與密碼相符"""
        return password == self.password
    