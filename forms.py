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

