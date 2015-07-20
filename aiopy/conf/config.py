# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "Configure",
]

"""

Define conf interface

"""

from aiopy.conf.method import OnlineDict, MergeDict, Configure2Dict

def Configure(develop, online = None):
    config = OnlineDict(MergeDict(Configure2Dict(develop,'develop'),Configure2Dict(online,'online'))) if online else OnlineDict(Configure2Dict(develop,'develop'))
    return config
