from flask import render_template, flash, redirect
from app import app
from .forms import QueryForm

@app.route('/')
@app.route('/index')
def index():
    form = QueryForm()
    return render_template('query.html',
                            title='Star Wars Trivia Bot',
                            form=form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm()
    if form.validate_on_submit():
        flash('Query requested for %s' % (form.query.data))

    return redirect('/index')
