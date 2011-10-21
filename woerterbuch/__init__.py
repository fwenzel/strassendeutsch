from flask import Flask
app = Flask(__name__)
app.config.from_object('woerterbuch.settings')

import woerterbuch.views
