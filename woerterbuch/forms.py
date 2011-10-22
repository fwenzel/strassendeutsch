# -*- coding: utf-8 -*-
from flaskext.wtf import (Form, TextField, TextAreaField, TextInput, Required,
                          Length, validators)
from flaskext.wtf.html5 import EmailField
from wtforms.fields import Field


# Validator messages
REQ_MSG = u'Dieses Feld darf nicht leer sein.'
LEN_MSG = u'Dieses Feld muss zwischen %(min)d und %(max)d Zeichen lang sein.'


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


def tags_validator(form, field):
    """
    Make sure a list of tags contains at least five tags, and the tags
    themselves are between 2 and 20 characters.
    """
    tags = field.data
    try:
        assert len(tags) >= 5
        for tag in tags:
            assert 2 < len(tag) < 20
    except AssertionError:
        raise validators.ValidationError(
            u'Du musst mindestens 5 Schlüsselworte eingeben. Jedes davon '
            u'darf höchstens 20 Zeichen lang sein.')


class NewWordForm(Form):
    title = TextField(u'Mein neues Wort', [Required(message=REQ_MSG),
                                           Length(min=3, max=50, message=LEN_MSG)])
    definition = TextAreaField(u'Definition', [Required(message=REQ_MSG)])
    tags = TagListField(u'Schlüsselworte', [Required(message=REQ_MSG),
                                            tags_validator])
    email = EmailField(u'E-Mail', [Required(message=REQ_MSG),
                                   validators.email()])
    nickname = TextField(u'Spitzname', [Required(message=REQ_MSG),
                                        Length(min=3, max=30, message=LEN_MSG)])
