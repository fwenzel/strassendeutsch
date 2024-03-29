from flask import Flask
from flaskext.cache import Cache
from flaskext.mongokit import BSONObjectIdConverter
from werkzeug.routing import BaseConverter

import settings

app = Flask(__name__)
app.config.from_object('woerterbuch.settings')
app.secret_key = settings.SECRET_KEY


## Hook up custom URL converters.
class RegexConverter(BaseConverter):
    """Regex-powered url converter."""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

app.url_map.converters['ObjectId'] = BSONObjectIdConverter


# Caching
cache = Cache(app)


# Templates
import woerterbuch.context_processors

# Views
import woerterbuch.views
