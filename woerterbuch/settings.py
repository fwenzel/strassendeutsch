## Database settings
MONGODB_DATABASE = 'woerterbuch'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None


## Session settings (set this!)
SECRET_KEY = None


## Flask-WTF
CSRF_ENABLED = True
#CSRF_SESSION_KEY = _csrf_token


## Import local config file, if it exists.
try:
    from woerterbuch.settings_local import *
except ImportError:
    pass
