from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime


def nocache(views):
    @wraps(views)
    def no_cache(*args, **kwargs):
        response = make_response(views(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, views)