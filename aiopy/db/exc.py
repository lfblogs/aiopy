# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "select",
    "execute"
]

"""
"""


import asyncio
import logging

logging.basicConfig(level=logging.INFO)

@asyncio.coroutine
def select(sql, args, size=None):
    logging.info('SQL: {}'.format(sql))
    global __pool
    with (yield from __pool) as conn:
        cursor = yield from conn.cursor()
        yield from cursor.execute(sql.replace('?', '%s'), args or ())
        value = (yield from cursor.fetchmany(size)) if size else (yield from cursor.fetchall())
        yield from cursor.close()
        logging.info('rows return: {}'.format(value))
        return value

@asyncio.coroutine
def execute(sql, args, autocommit=True):
    logging.info('SQL: {}'.format(sql))
    with (yield from __pool) as conn:
        if not autocommit:
            yield from conn.begin()
        try:
            cursor = yield from conn.cursor()
            yield from cursor.execute(sql.replace('?', '%s'), args)
            affected = cursor.rowcount
            yield from cursor.close()
            if not autocommit:
                yield from conn.commit()
        except BaseException as e:
            if not autocommit:
                yield from conn.rollback()
            raise
        return affected
