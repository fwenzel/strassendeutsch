# -*- coding: utf-8 -*-
from datetime import datetime
import os
import re

from flask import url_for
from flaskext.mongokit import MongoKit, Document
from mongokit import ValidationError

from woerterbuch import app
from woerterbuch.utils import slugify


class Word(Document):
    """A single dictionary entry."""
    __collection__ = 'words'
    structure = {
        'title': unicode,
        'definition': unicode,
        'tags': [unicode],
        'user': {
            'email': unicode,
            'nickname': unicode,
        },
        'votes': {
            'up': int,
            'down': int,
        },
        'url': {
            'token': unicode,
            'slug': unicode,
        },
        'created': datetime,
    }
    required_fields = ['title', 'definition', 'user.email', 'user.nickname',
                       'tags', 'url.slug', 'url.token']
    default_values = {
        'created': datetime.utcnow,
        'votes.up': 0,
        'votes.down': 0,
        'url.token': lambda: unicode(os.urandom(3).encode('hex')),
    }
    use_dot_notation = True
    indexes = [
        {'fields': ['title', 'user.email'],
         'unique': True},
        {'fields': ['url.token', 'url.slug'],},
    ]

    def save(self, *args, **kwargs):
        self.url.slug = slugify(self.title)
        super(Word, self).save(*args, **kwargs)

    @property
    def to_url(self):
        """(Relative) URL for this word."""
        return url_for('detail', slug=self.url.slug,
                       token=self.url.token)

db = MongoKit(app)
db.register([Word])
