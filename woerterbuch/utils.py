import re


def slugify(value):
    """Turn a unicode string into something URLable."""
    pattern = re.compile('[^\w\s-]', re.UNICODE)
    value = unicode(pattern.sub('-', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
