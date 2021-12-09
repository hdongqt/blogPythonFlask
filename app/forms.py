from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Tên đăng nhập',validators=[DataRequired(), Length(min=2, max=20)])
    fullname= StringField('Họ tên',validators=[DataRequired(), Length(min=5, max=35)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Đăng ký')


class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Đăng nhập')

class UpdateAccountForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=2, max=20)])
    fullname = StringField('Họ tên', validators=[DataRequired(), Length(min=5, max=35)])                       
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Avatar', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Cập nhật')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Tên đăng nhập đã được sử dụng. Vui lòng chọn tên đăng nhập khác.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email đã được sử dụng. Vui lòng chọn Email khác.')

class PostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    picture = FileField('Hình ảnh', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Xác nhận')