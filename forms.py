from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()], widget=TextArea())


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
