from flask.ext.wtf import Form, PasswordField, Email, Required, TextField
from flask.ext.wtf.html5 import EmailField


class RegistrationForm(Form):
    email = EmailField('Email', validators=[Email(), Required()])
    password = PasswordField('Password', validators=[Required()])


class LoginForm(Form):
    email = EmailField('Email', validators=[Email(), Required()])
    password = PasswordField('Password', validators=[Required()])


class UpdateForm(Form):
    ssn = TextField('SSN', validators=[Required()])
    code = PasswordField('Code', validators=[Required()])
