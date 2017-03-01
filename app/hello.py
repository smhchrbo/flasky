from flask import Flask,request,redirect,abort,render_template
from flask_script import  Manager
from flask_bootstrap import Bootstrap
from flask_moment import  Moment
from datetime import  datetime
from flask_wtf import Form
from wtforms import  StringField,SubmitField
from wtforms.validators import DataRequired

class NameForm(Form):
    name = StringField("your name:",validators=[DataRequired()])
    pwd = StringField("your pwd:",validators=[DataRequired()])
    submit = SubmitField('submit')


app = Flask(__name__)
app.config['SECRET_KEY']='asdfg'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/",methods=['GET', 'POST'])
def index():
    name = None
    pwd = None
    form =NameForm()
    if form.validate_on_submit():
        name = form.name.data
        pwd = form.pwd.data
        form.name.data = ''
        form.pwd.data = ''
    return render_template("index.html",form = form,name = name,pwd = pwd)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html",name = name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 404

if __name__ == "__main__":
    #app.run(debug = True)
    manager.run()

#CC:redirect and session