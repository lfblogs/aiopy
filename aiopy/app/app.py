# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = []

"""
"""

import os
import sys
import asyncio
try:
    from aiohttp import web
except ImportError:
    from aiopy.required.aiohttp import web
from aiopy.db import Pool
from aiopy.http import AddTemplates, AddStatic, AddRoutes
from aiopy.app.factory import logger_factory, response_factory, data_factory
from aiopy.app.filter import datetime_filter
from aiopy.conf import Configure

import logging
logging.basicConfig(level=logging.INFO)

class App:
    def __init__(self, develop, online=None, *args):
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())
        config = Configure(develop,online)
        logging.info(config)
        self.loop = asyncio.get_event_loop()
        self.config = config
        self.args = args
        self.initiation()
        global app
        lst = [logger_factory, response_factory,data_factory]
        [lst.append(i) for i in args]
        app = web.Application(loop=self.loop, middlewares=lst)
        AddTemplates(app, self.config.templates, filters=dict(datetime=datetime_filter))
        AddStatic(app, self.config.static)
    def initiation(self):
        yield from Pool(loop=self.loop, **self.config.db)
    def add_route(self, route_name):
        AddRoutes(app, route_name)
    def run(self, ip='127.0.0.1' , port=8801):
        srv = yield from self.loop.create_server(app.make_handler(), ip, port)
        logging.info('server started at http://{}:{}...'.format(ip,port))
        return srv
