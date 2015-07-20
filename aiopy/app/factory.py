# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "logger_factory",
    "data_factory",
    "response_factory",
]

"""
"""


import asyncio
import json
try:
    from aiohttp import web
except ImportError:
    from aiopy.required.aiohttp import web
import logging

@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (yield from handler(request))
    return logger

@asyncio.coroutine
def data_factory(app, handler):
    @asyncio.coroutine
    def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = yield from request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = yield from request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (yield from handler(request))
    return parse_data

@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info('Response handler...')
        r = yield from handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = False
                try:
                    r['__user__'] = request.__user__
                except:
                    r['__user__'] = ''
                if isinstance(app['__templating__'], list):

                    for index,i in enumerate(app['__templating__']):
                        try:
                            app['__templating__'][index].get_template(template)
                        except:
                            pass
                        else:
                            resp = web.Response(body=app['__templating__'][index].get_template(template).render(**r).encode('utf-8'))
                            resp.content_type = 'text/html;charset=utf-8'
                            break
                else:
                    resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                    resp.content_type = 'text/html;charset=utf-8'
                if resp:
                    return resp
                else:
                    raise FileNotFoundError('template file {} is not found'.format(template))
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

