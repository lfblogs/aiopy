# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "APIError",
    "APIValueError",
    "APIPermissionError",
    "APIResourceNotFoundError",
    "error",
]

"""

Adduction API Error.

"""

from aiopy.api.error import APIError, APIValueError, APIPermissionError, APIResourceNotFoundError