# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "GET",
    "POST"
]

"""

Define decorator:GET, POST

"""

import functools
import logging
try:
    import aiohttp
except ImportError:
    from aiopy.required import aiohttp

logging.basicConfig(level=logging.INFO)

def GET(path):
    """
        Define decorator @get('/path'):
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def POST(path):
    """
        Define decorator @post('/path'):
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

def Response():
    return aiohttp.web.Response()