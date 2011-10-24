# -*- coding: utf-8 -*-
from flask import request, render_template, redirect, url_for, flash
from jinja2 import Markup
from pymongo.errors import DuplicateKeyError

from woerterbuch import app
from woerterbuch.forms import NewWordForm
from woerterbuch.models import db


@app.route('/')
def index():
    """Front page."""
    words = [db.Word.find_random() for i in xrange(3)]
    return render_template('index.html', words=words)


@app.route('/new', methods=("GET", "POST"))
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
        try:
            word.save()
        except DuplicateKeyError:
            flash(Markup(
                u'<strong>Hoppla!</strong> Sieht so aus, als ob wir deine '
                u'Definition schon haben!'), 'error')
        except Exception, e:
            flash(Markup(
                u'<strong>Ohje!</strong> Beim Speichern ist etwas schief '
                u'gelaufen. Bitte versuch es noch einmal, und falls alles '
                u'nichts hilft, sag uns bescheid und erwähne diesen Fehler: '
                u'<em>%s</em>') % e, 'error')
        else:
            flash(Markup(u'<strong>Hurra!</strong> Vielen Dank für dieses '
                         u'neue Wort!'), 'success')
            return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/<slug>-<regex("[0-9a-f]{6}"):token>')
def detail(slug, token):
    """Detail page for a single word."""
    word = db.Word.find_one_or_404({'url.slug': slug, 'url.token': token})
    return render_template('detail.html', word=word)


@app.route('/vote/<regex("[01]"):up>/<ObjectId:id>',
           methods=('GET', 'POST'))
def vote(up, id):
    """Vote up/down for a single word. AJAX action."""
    direction = 'votes.up' if int(up) else 'votes.down'
    word = db.Word.get_or_404(id)
    db.Word.collection.update({'_id': id}, {"$inc" : { direction: 1 }})

    if not request.is_xhr:
        flash(u'Danke für deine Stimme!', 'success')
        return redirect(word.to_url)
