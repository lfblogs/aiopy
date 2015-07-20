# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "GET",
    "POST",
    "AddRoute"
    "AddRoutes",
    "AddStatic",
    "AddTemplates",
    "exc",
    "handlers",
    "request"
]

"""

Adduction http method.

"""

from aiopy.http.request import GET, POST
from aiopy.http.exc import AddRoute, AddRoutes, AddStatic, AddTemplates
