from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from personalBlog.models.user import User

class RegistrationForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(message='user_id不能為空')])
    email = StringField('Email', validators=[DataRequired(message='email不能為空'), Email(message='email格式不符')])
    password = PasswordField('Password', validators=[
        DataRequired(message='密碼不能為空'),
        Length(min=8, message='密碼必須大於8個字'),
        Regexp(r'^(?=.*[A-Za-z]).*$', message='密碼必須包含至少一個字母'),
        Regexp(r'^(?=.*[!@#$%^&*()]).*$', message='密碼必須包含至少一個特殊字元'),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='密碼不相同')])

    def validate_user_id(self, field):
        if User.query.filter_by(user_id=field.data).first():
            raise ValidationError('user_id已經存在 請重新輸入')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email已經存在，請重新輸入')
        
class LoginForm(FlaskForm):
    user_id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
