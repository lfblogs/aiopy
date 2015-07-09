#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 3.4.x
# Last Modified: 2015/7/9 1:38


__all__ = []
__author__ = "lfblogs (email:13701242710@163.com)"
__version__ = "1.0.1"

import asyncio
import os
import json
import inspect
import functools
import time

from jinja2 import Environment,FileSystemLoader
from datetime import datetime
from urllib import parse
from aiohttp import web
from Pyaio.apis.Error import APIError
from Pyaio.http.handlers import RequestHandler
import logging

logging.basicConfig(level=logging.INFO)

def get(path):
    '''
        Define decorator @get('/path'):
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
        Define decorator @post('/path'):
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


def add_templates(app, **kw):
    logging.info('init templates...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        raise ValueError('template dir is not define.')
    filters = kw.get('filters', None)

    if isinstance(path,list):
        env = []
        for i in path:
            logging.info('set template path: {}'.format(i))
            env_ = Environment(loader=FileSystemLoader(i), **options)
            if filters is not None:
                for name, f in filters.items():
                    env_.filters[name] = f
            env.append(env_)
    else:
        logging.info('set template path: {}'.format(path))
        env = Environment(loader=FileSystemLoader(path), **options)
        if filters is not None:
            for name, f in filters.items():
                env.filters[name] = f
    app['__templating__'] = env

def add_static(app,path):
    if isinstance(path,dict):
        for k, v in path.items():
            app.router.add_static(k, v)
    else:
        app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))

def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)
