## Database settings
MONGODB_DATABASE = 'woerterbuch'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None


## Import local config file, if it exists.
try:
    from woerterbuch.settings_local import *
except ImportError:
    pass
