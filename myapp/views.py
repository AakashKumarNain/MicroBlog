from myapp import app
from flask import render_template

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
