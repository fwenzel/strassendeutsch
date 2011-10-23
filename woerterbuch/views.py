from flask import request, render_template, redirect, url_for

from woerterbuch import app
from woerterbuch.forms import NewWordForm
from woerterbuch.models import db

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=["GET", "POST"])
def new_word():
    form = NewWordForm(request.form)
    if form.validate_on_submit():
        word = db.Word()
        word.title = form.title.data
        word.definition = form.definition.data
        word.tags = form.tags.data
        word.user.email = form.email.data
        word.user.nickname = form.nickname.data
        word.save()
        #flash("Success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)
