# -*- coding: utf-8 -*-
from flask import request, render_template, redirect, url_for, flash, abort
from jinja2 import Markup
import pymongo
from pymongo.errors import DuplicateKeyError

from woerterbuch import app, cache
from woerterbuch.forms import NewWordForm
from woerterbuch.models import db


@app.route('/')
def index():
    """Front page."""
    words = db.Word.find_randomized({'votes.up': {'$gte': 3}}).limit(3)
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
           methods=('GET', 'POST'), defaults={'vote_new': False})
@app.route('/vote/new/<regex("[012]"):up>/<ObjectId:id>',
           methods=('GET', 'POST'), defaults={'vote_new': True})
def vote(up, id, vote_new):
    """
    Vote up/down for a single word. AJAX action.
    Possible votes: 0 = vote down
                    1 = vote up
                    2 = don't know
    """
    word = db.Word.get_or_404(id)

    vote_up = int(up)  # 0, 1, or 2
    directions = ('votes.down', 'votes.up')

    # Remember votes, do not allow double voting.
    # We cache: '<ip_addr>:<wordid> => [01]', e.g.: '127.0.0.1:43a...0001 => 1'
    ip = request.remote_addr
    vote = cache.get('%s:%s' % (ip, id))
    if not vote or vote != up:
        to_update = {}  # Pending DB updates.

        # Count a vote unless this is a "don't know".
        if up != '2':
            # If previously voted, update vote, do not recount.
            if up not in (vote, '2'):
                to_update[directions[int(not vote_up)]] = -1

            # Cast vote now.
            to_update[directions[vote_up]] = 1

            db.Word.collection.update({'_id': id}, {"$inc": to_update})

        # ... and remember this.
        cache.set('%s:%s' % (ip, id), up,
                  timeout=app.config['CACHE_VOTE_TIMEOUT'])

    if not request.is_xhr:
        flash(u'Danke für deine Stimme!', 'success')
        if vote_new:
            return redirect(url_for('vote_new'))
        else:
            return redirect(word.to_url)
    else:
        return 'ok'


@app.route('/vote/new')
def vote_new():
    """Vote on new submissions."""
    words = db.Word.find({'$and': [{'votes.up': {'$lt': 3}},
                                   {'votes.down': {'$lt': 3}}]},
                         sort=[('url.token', pymongo.ASCENDING)])

    # Find a word that's not been voted on yet
    ip = request.remote_addr
    myword = None
    for word in words:
        if cache.get('%s:%s' % (ip, word._id)) is None:
            myword = word
            break

    return render_template('vote_new.html', word=myword)
