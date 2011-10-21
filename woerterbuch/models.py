# -*- coding: utf-8 -*-
from datetime import datetime
import re

from flaskext.mongokit import MongoKit, Document

from woerterbuch import app


def email_validator(value):
    """Validate an email address."""
    email = re.compile(
        r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)",
        re.IGNORECASE)
    if not email.match(value):
        raise ValidatorError(u"%s ist keine gültige E-Mail-Adresse.")


def tags_validator(tags):
    """
    Make sure a list of tags contains at least five tags, and the tags
    themselves are between 2 and 20 characters.
    """
    assert len(tags) >= 5
    for tag in tags:
        assert 2 < len(tag) < 20


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

    validators = {
        'user.email': email_validator,
        'tags': tags_validator,
    }
    use_dot_notation = True


db = MongoKit(app)
db.register([Word])
