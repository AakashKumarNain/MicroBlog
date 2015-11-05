from myapp import app , lm, oid
from flask import render_template, flash, redirect, session, request, url_for, g
from flask.ext.login import login_user , logout_user , current_user , login_required
from .forms import LoginForm
from .models import User,db

@lm.user_loader
def load_user(id):
    return User.objects.get(id = id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def hello():
    return "Hello Nain"

@app.route('/index')
@login_required
def index():
    user = g.user
    title = 'Welcome'
    return render_template('index.html',
                           user = user,
                           title=title,
                           posts=user.post,
                           email=user.email)


@app.route('/login', methods =['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data , ask_for=['nickname','email'])
       ## flash('Login requested for ID = "%s" , remember_me = %s'  %(form.openid.data,str(form.remember_me.data)))
       ##return redirect('/index')

    return render_template('login.html',title='Sign In',form=form , providers = app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email=="":
        flash("Invalid login")
        return redirect (url_for('login'))

    user = User.objects.get(email=resp.email)

    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]

        user = User(nickname = nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False

    if 'remember_me' in session :
        remember_me = session['remember_me']
        session.pop('remember_me',None)

    login_user(user , remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
