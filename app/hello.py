from flask import Flask,request,redirect,abort,render_template,session,url_for,flash
from flask_script import  Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import  Moment
from datetime import  datetime


from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import  Migrate,MigrateCommand
from flask_mail import Mail,Message
from threading import Thread







app = Flask(__name__)
app.config['SECRET_KEY']='asdfg'
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

#配置使用gmail
#app.config['MAIL_SERVER']='smtp.googlemail.com'
#app.config['MAIL_PORT']='587'
#app.config['MAIL_USE_TLS']=True
#app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')

#集成电子邮件功能
#异步
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[flasky]'
app.config['FLASY_MAIL_SENDER']='flasky admin <flasky@example.com>'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
def send_email(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                sender=app.config['FLASY_MAIL_SENDER'],
                recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return  thr

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)




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
            if app.config['FLASKY_ADMIN']:
                    send_email(app.config['FLASKY_ADMIN'],'NEW_USER','MAIL_NEWUSER',user=user)
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
    app.run(debug = True)
    #manager.run()
    

#CC:redirect and session
