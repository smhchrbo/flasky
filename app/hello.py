from flask import Flask,request,redirect,abort,render_template,session,url_for,flash
from flask_script import  Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import  Moment
from datetime import  datetime
from flask_wtf import Form
from wtforms import  StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import  Migrate,MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))

class NameForm(Form):
    name = StringField("your name:",validators=[DataRequired()])
    #pwd = StringField("your pwd:",validators=[DataRequired()])
    submit = SubmitField('submit')


app = Flask(__name__)
app.config['SECRET_KEY']='asdfg'
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True




manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

class Role(db.Model):
    __tablename__ ='role'
    id=db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(64),unique=True)

    user=db.relationship('User',backref='role')
    
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ ='user'
    id=db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(64),unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/",methods=['GET', 'POST'])
def index():
    name = None

    form =NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    
    return render_template("index.html",form = form,name = session.get('name'),known=session.get('known',False))

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)


manager.add_command("shell",Shell(make_context=make_shell_context))




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
