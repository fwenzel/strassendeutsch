#!/usr/bin/env python
import random
import string
import sys

from elasticutils import es_required
from flaskext.script import Manager
from mongokit import Connection
import pymongo
from pymongo.errors import DuplicateKeyError

from woerterbuch import app, elastic
from woerterbuch.models import db



manager = Manager(app)


@manager.command
def ensure_indexes():
    """Set/ensure indexes on MongoDB database."""
    db_name = app.config['MONGODB_DATABASE']
    connection = Connection()
    for doc in db.registered_documents:
        for idx in doc.indexes:
            idxdef = [(f, pymongo.ASCENDING) for f in idx['fields']]
            unique = idx.get('unique', False)
            getattr(connection[db_name], doc.__collection__).ensure_index(
                idxdef, unique=unique, dropDups=True)
    sys.stderr.write("Done\n")


@manager.command
@manager.option('-n', '--number', dest='num', required=False)
def create_test_data(num=20):
    """Create a number of random words to test with."""
    created = 0
    for i in xrange(int(num)):
        title = unicode(''.join(random.sample(string.ascii_letters,
                                              random.randint(2, 10))))
        tags = [unicode(''.join(random.sample(string.ascii_letters,
                                              random.randint(2, 10))))
                for t in xrange(5)]
        tags.append(u'testdata')

        word = db.Word()
        word.title = u'Test_%s' % title
        word.definition = u' '.join(title for _ in
                                    xrange(random.randint(3, 30)))
        word.tags = tags
        word.user.email = u'%s@example.com' % title
        word.user.nickname = u'user_%s' % title

        word.votes.up = random.randint(0, 10)
        word.votes.down = random.randint(0, 10)

        try:
            word.save()
        except DuplicateKeyError:
            pass
        else:
            created += 1
    sys.stderr.write("Done: Created %d entries.\n" % created)


@manager.command
@es_required
def reindex(es):
    """Reindex all relevant words in ElasticSearch."""
    es.delete_index_if_exists(app.config['ES_INDEX'])
    es.create_index_if_missing(app.config['ES_INDEX'])

    words = db.Word.find({'votes.up': {'$gte': app.config['MIN_VOTES']}})
    for word in words:
        elastic.index_word(word=word, force=True)
    sys.stderr.write("Done: Indexed %d words.\n" % words.count())


if __name__ == "__main__":
        manager.run()
