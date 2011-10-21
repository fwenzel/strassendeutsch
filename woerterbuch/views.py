from flask import render_template

from woerterbuch import app
from woerterbuch.models import db

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new', methods=["GET", "POST"])
def new_word():
    return render_template('new.html')
