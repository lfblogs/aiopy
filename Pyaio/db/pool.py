#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 3.4.x
# Last Modified: 2015/7/8 23:40


__all__ = []
__author__ = "lfblogs (email:13701242710@163.com)"
__version__ = "1.0.1"


import asyncio
import aiomysql
import logging

logging.basicConfig(level=logging.INFO)

@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('Create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host = kw.get('host', ''),
        port = kw.get('port', 3306),
        user = kw.get('user', ''),
        password = kw.get('password', ''),
        db = kw.get('db', ''),
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
    )

@asyncio.coroutine
def select(sql, args, size=None):
    logging.info('SQL: {}'.format(sql))
    global __pool
    with (yield from __pool) as conn:
        cursor = yield from conn.cursor(aiomysql.DictCursor)
        yield from cursor.execute(sql.replace('?', '%s'), args or ())
        value = (yield from cursor.fetchmany(size)) if size else (yield from cursor.fetchall())
        yield from cursor.close()
        logging.info('rows returned: {}'.format(value))
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

