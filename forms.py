from flask_wtf import FlaskForm as Form

from wtforms import validators
from wtforms.fields import StringField, IntegerField, DateTimeField, SelectField, PasswordField

#from wtforms.fields.html5 import EmailField
#pn_regex = re.compile(r"^[0-9]{8}-[0-9]{4}$")



class ProductForm(Form):
    name = StringField('Name', validators=[validators.InputRequired()])
    description = StringField('Description', validators=[validators.InputRequired()])
    cost = IntegerField('Cost', validators=[validators.InputRequired()])

class SearchForm(Form):
    search = StringField('Search', validators=[validators.InputRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = StringField('Password', validators=[validators.InputRequired()])

"""
class AdminLoginForm(Form):
    user = StringField('Username', validators=[validators.InputRequired(), user_validator])
    password = PasswordField(
            'Password',
            validators=[
                validators.InputRequired(),
                validators.EqualTo('password_confirm', message='Passwords must be equal')])
    password_confirm = PasswordField('Password confirm')
    """
