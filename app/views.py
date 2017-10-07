import datetime
from flask import render_template, flash, redirect, request, url_for, session
from app import app, db, models
from .forms import InputWordForm
from morph.morph_analysis import pars_analyse
from morph.morph_analysis import tag_interpretation
#Home
@app.route('/')
def index():
    return render_template('home.html')

#About
@app.route('/about_project')
def about_project():
    return render_template('about.html')

@app.route('/about_turki')
def about_turki():
    return render_template('turki.html')

@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')

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
        word = form.word.data.lower()
    result = []
    parses = pars_analyse(word)
    if parses == []:
        return render_template('analysis.html', word=word, res=result)
    else:
        for p in parses:
            if len(p) < 2:
                tmp_int = {}
                for i in [0,1,2]:
                    tmp_int[i] = tag_interpretation(p, i)
                result.append(([p[0][0]+'+∅', ' + '.join(([str(m) for m in p]))], tmp_int))
            else:
                tmp = []
                tmp_int = {}
                for morpheme in p:
                    tmp.append(morpheme[0])
                for i in [0,1,2]:
                    tmp_int[i] = tag_interpretation(p, i)
                result.append((['+'.join(tmp), ' + '.join([str(m) for m in p])], tmp_int))
        return render_template('analysis.html', word=word, res=result)
