from flask import request, render_template, redirect, url_for

from woerterbuch import app
from woerterbuch.forms import NewWordForm
from woerterbuch.models import db

@app.route('/')
def index():
    """Front page."""
    words = [db.Word.find_random() for i in xrange(3)]
    return render_template('index.html', words=words)


@app.route('/new', methods=["GET", "POST"])
def new_word():
    """New word submission."""
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


@app.route('/<slug>-<regex("[0-9a-f]{6}"):token>')
def detail(slug, token):
    word = db.Word.find_one_or_404({'url.slug': slug, 'url.token': token})
    return render_template('detail.html', word=word)
