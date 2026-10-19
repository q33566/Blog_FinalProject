from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, StringField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from personalBlog.extensions import db
from personalBlog.models import User


class RegistrationForm(FlaskForm):
    user_id = StringField('帳號', validators=[DataRequired(message='請輸入帳號'), Length(max=30)])
    email = StringField('Email', validators=[DataRequired(message='請輸入 Email'), Email(message='Email 格式不正確')])
    password = PasswordField('密碼', validators=[
        DataRequired(message='請輸入密碼'),
        Length(min=8, message='密碼至少要 8 個字元'),
        Regexp(r'^(?=.*[A-Za-z]).*$', message='密碼需要包含至少一個英文字母'),
        Regexp(r'^(?=.*[!@#$%^&*()]).*$', message='密碼需要包含至少一個特殊字元，例如 ! @ #'),
    ])
    confirm_password = PasswordField('確認密碼', validators=[EqualTo('password', message='兩次輸入的密碼不一致')])

    def validate_user_id(self, field):
        if db.session.get(User, field.data):
            raise ValidationError('這個帳號已經有人使用')

    def validate_email(self, field):
        if db.session.scalar(db.select(User).filter_by(email=field.data)):
            raise ValidationError('這個 Email 已經註冊過')


class LoginForm(FlaskForm):
    user_id = StringField('帳號', validators=[DataRequired(message='請輸入帳號')])
    password = PasswordField('密碼', validators=[DataRequired(message='請輸入密碼')])


class AboutForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired(message='請輸入名字'), Length(max=50)])
    about_me = TextAreaField('自我介紹', validators=[DataRequired(message='請輸入自我介紹')],
                             render_kw={'rows': 8})
    picture = FileField('大頭貼（jpg / png）',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'], '只允許上傳 jpg 或 png 格式的圖片')])
    email = StringField('Email', validators=[DataRequired('請輸入 Email'), Email('Email 格式不正確')])


class ArticleForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired(message='這個欄位必填'), Length(max=100)])
    tags = StringField('分類（以逗號分隔）', validators=[DataRequired(message='這個欄位必填'), Length(max=200)])
    intro = StringField('簡介', validators=[DataRequired(message='這個欄位必填'), Length(max=200)])
    content = TextAreaField('內容', validators=[DataRequired(message='這個欄位必填')])


class CommentForm(FlaskForm):
    content = TextAreaField('留言', validators=[DataRequired(message='留言不能空白'), Length(max=500)])
