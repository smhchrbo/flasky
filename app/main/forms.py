from flask_wtf import Form
from wtforms import  StringField,SubmitField
from wtforms.validators import DataRequired

class NameForm(Form):
    name = StringField("your name:",validators=[DataRequired()])
    #pwd = StringField("your pwd:",validators=[DataRequired()])
    submit = SubmitField('submit')