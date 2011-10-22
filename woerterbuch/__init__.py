from flask import Flask

from woerterbuch import settings


app = Flask(__name__)
app.config.from_object('woerterbuch.settings')
app.secret_key = settings.SECRET_KEY

import woerterbuch.views
