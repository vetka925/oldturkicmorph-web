import datetime
from flask import render_template, flash, redirect, request, url_for, session
from app import app, db, models
from .forms import InputWordForm
from passlib.hash import sha256_crypt
from morph.parsing import Parsing
#Home
@app.route('/')
def index():
    return render_template('home.html')

#About
@app.route('/about')
def about():
    return render_template('about.html')

#Articles
@app.route('/articles')
def articles():
    return render_template('articles.html', articles=articles)

#Article
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

#Registrtion
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #commit to db
        user = models.User(name=name, email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        redirect(url_for('index'))
        flash = ('Вы зарегестрированы и теперь можете войти', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form )

@app.route('/morph')
def morph():
    form = InputWordForm(request.form)
    if request.method == 'POST' and form.validate():
        word = form.word.data
    return render_template('morph.html', form=form)

@app.route('/morph', methods=['POST'])
def analysis():
    form = InputWordForm(request.form)
    if form.validate():
        word = form.word.data
    parse = Parsing(word)
    ma = parse.morph_analysis(1)
    return render_template('analysis.html', word=word, ma=ma)
