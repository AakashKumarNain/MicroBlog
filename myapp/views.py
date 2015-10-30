from myapp import app
from flask import render_template,flash,redirect
from .forms import LoginForm

@app.route('/')
def hello():
    return "Hello Nain"

@app.route('/index')
def index():
    user = {'name' : 'Aakash Nain'}
    title = "Nain's Blog"
    posts = [
        { 
            'author': {'name': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'name': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',
                           user = user,
                           title=title,
                           posts=posts)


@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for ID = "%s" , remember_me = %s'  %(form.openid.data,str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',title='Sign In',form=form)

