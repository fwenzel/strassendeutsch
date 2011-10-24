#!/usr/bin/env python
"""Set indexes on MongoDB."""
from mongokit import Connection
import pymongo

from woerterbuch import app
from woerterbuch.models import db


db_name = app.config['MONGODB_DATABASE']
connection = Connection()
for doc in db.registered_documents:
    for idx in doc.indexes:
        idxdef = [(f, pymongo.ASCENDING) for f in idx['fields']]
        unique = idx.get('unique', False)
        getattr(connection[db_name], doc.__collection__).ensure_index(
            idxdef, unique=unique, dropDups=True)
