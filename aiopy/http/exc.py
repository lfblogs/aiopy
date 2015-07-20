# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "AddRoute",
    "AddRoutes",
    "AddStatic",
    "AddTemplates"
]

"""

Define url and template

"""

import asyncio
import inspect
import logging
from jinja2 import Environment,FileSystemLoader
from aiopy.http.handlers import RequestHandler

logging.basicConfig(level=logging.INFO)


def AddTemplates(app ,path=None,**kw):
    logging.info('initialization templates conf...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    if path is None:
        raise ValueError('template dir is not define.')
    filters = kw.get('filters', None)

    if isinstance(path, list):
        env = []
        for i in path:
            logging.info('Set template path: {}'.format(i))
            env_ = Environment(loader=FileSystemLoader(i), **options)
            if filters is not None:
                for name, f in filters.items():
                    env_.filters[name] = f
            env.append(env_)
    else:
        logging.info('Set template path: {}'.format(path))
        env = Environment(loader=FileSystemLoader(path), **options)
        if filters is not None:
            for name, f in filters.items():
                env.filters[name] = f
    app['__templating__'] = env

def AddStatic(app,path):
    if isinstance(path,dict):
        for k, v in path.items():
            app.router.add_static(k, v)
    else:
        app.router.add_static('/static/', path)
    logging.info('Add static url %s => %s' % ('/static/', path))

def AddRoute(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@GET or @POST not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('Add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

def AddRoutes(app, module_name):
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
                AddRoute(app, fn)




