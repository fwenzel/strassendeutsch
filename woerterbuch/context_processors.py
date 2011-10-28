# -*- coding: utf-8 -*-
import jinja2

from woerterbuch import app


@app.context_processor
def inject_wordmark():
    return {'strassendeutsch': jinja2.Markup(
        u'<span class="wordmark">Straßendeutsch</span>')}
