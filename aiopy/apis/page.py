#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 3.4.x
# Last Modified: 2015/7/9 1:32


__all__ = []
__author__ = "lfblogs (email:13701242710@163.com)"
__version__ = "1.0.1"

class Page(object):
    '''
    Page object for display pages.
    '''

    def __init__(self, item_count, page_index=1, page_size=10):
        '''
            Init Pagination by item_count page_index and page_size

        >>> p1 = Page(100, 1)
        >>> p1.page_count
        10
        >>> p1.offset
        0
        >>> p1.limit
        10
        >>> p2 = Page(90, 9, 10)
        >>> p2.page_count
        9
        >>> p2.offset
        80
        >>> p2.limit
        10
        >>> p3 = Page(91, 10, 10)
        >>> p3.page_count
        10
        >>> p3.offset
        90
        >>> p3.limit
        10
        '''

        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count
        if (item_count ==0) or (page_index > self.page_count):
            self.offset  = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: {}, page_count:{}, page_index:{}, page_size:{}, offset:{}, limit:{}, '.format(self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)
