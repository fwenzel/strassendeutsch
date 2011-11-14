from elasticutils import es_required

from woerterbuch import app


@es_required
def index_word(es, word, force=False):
    """Index a new word in the search engine."""
    if force or not word.in_es:
        es.index(word.to_es_json(), app.config['ES_INDEX'], 'word',
                 id=str(word._id), bulk=True)
        word.in_es = True
        word.save()


@es_required
def remove_word(es, word, force=False):
    """Remove a previously indexed word from the search index."""
    if force or word.in_es:
        es.delete(app.config['ES_INDEX'], 'word', str(word._id), bulk=True)
        word.in_es = False
        word.save()