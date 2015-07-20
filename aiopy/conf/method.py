# -*- coding: UTF-8 -*-

__author__ = "Liu Fei"
__github__ = "http://github.com/lfblogs"
__all__ = [
    "SimpleDict",
    "Configure2Dict",
    "MergeDict",
    "OnlineDict"
]

"""
"""


import os
import sys

class SimpleDict(dict):
    '''
        Simple dict but access support 'dict_name.key' style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(SimpleDict, self).__init__(**kw)
        for k, v in  zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return  self[key]
        except KeyError:
            raise AttributeError("'Dict' object has no attribute '{}'".format(key))

    def __setattr__(self, key, value):
        self[key] = value


def Configure2Dict(name,key=None):
    '''
        loading config, return dict
    '''
    config = {}
    name = __import__(name)
    if key == 'develop':
        for k, v in name.develop.__dict__.items():
            if k[0:2] != '__'  and k[-2:] != '__':
                config[k] = v
    elif key == 'online':
        for k, v in name.online.__dict__.items():
            if k[0:2] != '__'  and k[-2:] != '__':
                config[k] = v
    return config

def Configure2Dict_old(file):
    '''
        loading conifg file, return dict
    '''
    config = {}
    if not os.path.exists(file):
        raise FileNotFoundError("Configuration file '{}' is not found".format(file))
    elif not os.path.isfile(file):
        raise FileNotFoundError("Configuration file '{}' is not file".format(file))
    else:
        name = os.path.realpath(file).split(os.sep)[-1].split('.')[0]
        path = os.sep.join(os.path.realpath(file).split(os.sep)[0:-1])
        sys.path.append(path)
        name = __import__(name)
        for k, v in name.__dict__.items():
            if k[0:2] != '__'  and k[-2:] != '__':
                config[k] = v
        return config

def MergeDict(develop, online):
    '''
        merge dict
    '''
    d = {}
    for k, v in develop.items():
        if k in online:
            d[k] = MergeDict(v, online[k]) if isinstance(v, dict) else online[k]
        else:
            d[k] = v
    return d

def OnlineDict(d):
    '''
        online dict.
    '''
    simpledict = SimpleDict()
    for k, v in d.items():
        simpledict[k] = OnlineDict(v) if isinstance(v, dict) else v
    return simpledict
