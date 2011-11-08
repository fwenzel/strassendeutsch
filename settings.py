## Database settings
MONGODB_DATABASE = 'woerterbuch'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

## Session settings (set this to a random string!)
SECRET_KEY = None

## Flask-WTF(orms)
CSRF_ENABLED = True
#CSRF_SESSION_KEY = _csrf_token

## Flask-Cache
CACHE_TYPE = 'simple'  # or null, memcached, filesystem, ...
CACHE_KEY_PREFIX = 'wb:'
# CACHE_DIR  # filesystem cache only
CACHE_VOTE_TIMEOUT = 2 * 24 * 60 * 60  # (not part of Flask-Cache) Time until IP/word vote cache times out.

## Pagination
PER_PAGE = 20

## ElasticSearch settings
ES_HOSTS = ['127.0.0.1:9200']
ES_INDEXES = {'default': 'words',}
ES_DISABLED = False
ES_INDEX = 'words'

## Import local config file, if it exists.
try:
    from settings_local import *
except ImportError:
    pass
