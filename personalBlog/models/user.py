from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from personalBlog.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__  = 'USER_INFO'
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=True)
    email: Mapped[str] = mapped_column(String(30), nullable=True)
    password: Mapped[str] = mapped_column(String(30), nullable=True)
    
    def __init__(self, user_id, email, password):
        """初始化"""
        self.user_id = user_id
        self.email = email
        # 實際存入的為password_hash，而非password本身
        self.password_hash = password
    def get_id(self):
        return self.user_id
    
    def check_password(self, password):
        """檢查輸入是否與密碼相符"""
        return password == self.password
    