from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, NoneOf

from forms.custom_validators import EndsWith


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=5, max=20), NoneOf(values="#№@;: "),
                                                       EndsWith(".")])
    about = TextAreaField("Немного о себе", validators=[Length(min=0, max=140)])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditProfileForm(FlaskForm):
    name = StringField('Имя пользователя')
    about = TextAreaField("Немного о себе", validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить изменения')
