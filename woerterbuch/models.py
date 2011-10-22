# -*- coding: utf-8 -*-
from datetime import datetime
import re

from flaskext.mongokit import MongoKit, Document
from mongokit import ValidationError

from woerterbuch import app


class Word(Document):
    """A single dictionary entry."""
    __collection__ = 'words'
    structure = {
        'title': unicode,
        'definition': unicode,
        'created': datetime,
        'tags': [unicode],
        'user': {
            'email': unicode,
            'nickname': unicode,
        },
        'votes': {
            'up': int,
            'down': int,
        }
    }
    required_fields = ['title', 'definition', 'user.email', 'user.nickname',
                       'tags',]
    default_values = {
        'created': datetime.utcnow,
        'votes.up': 0,
        'votes.down': 0,
    }
    use_dot_notation = True


db = MongoKit(app)
db.register([Word])
