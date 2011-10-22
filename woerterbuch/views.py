from flask import request, render_template

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
        #flash("Success")
        pass
    return render_template('new.html', form=form)
