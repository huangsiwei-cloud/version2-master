from flask import render_template,flash,redirect,request,abort
from app import app
from .forms import LoginForm,SigninForm
from .models import *
from .DBManager import *

#db_manager=DBManager("mysql+mysqlconnector","47.107.86.216:3306","root","0C45313cea34","timecontrol")
db_manager = DBManager()
if db_manager is not None:
    print("DB is OK!")

@app.route('/')
@app.route('/index')
def home():
    form=LoginForm()
    return render_template("login.html",form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    db_session = db_manager.create_session()
    form = LoginForm()
    ac=form.account.data
    ps=form.password.data
    print(ac,ps)
    #检测表单的填写
    if form.validate_on_submit():
        if db_session.query(User).filter(ps==User.account).first is None:
            flash('This account is not exist')
            print('error 1')
            return render_template('login.html',form=form)
        elif ps != db_session.query(User).filter(ac==User.account).first().password:
            flash('Password is wrong')
            print('error 2')
            return render_template('login.html',form=form)
        else:
            print('hello')
            flash('Login requested, remember_me=' + str(form.remember_me.data))
            #return redirect('create_task.html')
            return render_template('create_task.html')
    db_session.close()


@app.route('/signin')
def signin():
    db_session=db_manager.create_session()
    form=SigninForm()
    ac=form.account.data
    ps1=form.password1.data
    ps2=form.password2.data
    #判断ac是否已经存在
    if form.validate_on_submit():
        if db_session.query(User).filter(ac==User.account).first() is not None:
            flash('This account already exists.')
            abort(101)
        else:
            user = User(account=ac,password=ps1)
            db_session.add(user)
            db_session.commit()
            flash('Sign up successfully')
            return redirect('/login')
    db_session.close()

@app.route('/tc')
def tc():
    return render_template('time_controler.html')

@app.route('/tomato')
def tomato():
    return render_template('tomato.html')

@app.route('/mail')
def mail():
    return render_template('time_controler-post.html')