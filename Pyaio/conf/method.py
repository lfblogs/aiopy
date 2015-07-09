#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 3.4.x
# Last Modified: 2015/7/8 23:22


__all__ = []
__author__ = "lfblogs (email:13701242710@163.com)"
__version__ = "1.0.1"

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


def Configure2Dict(file):
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

def MergeDict(default, prodution):
    '''
        merge dict
    '''
    d = {}
    for k, v in default.items():
        if k in prodution:
            d[k] = MergeDict(v, prodution[k]) if isinstance(v, dict) else prodution[k]
        else:
            d[k] = v
    return d

def ProduceDict(d):
    '''
        produce dict.
    '''
    simpledict = SimpleDict()
    for k, v in d.items():
        simpledict[k] = ProduceDict(v) if isinstance(v, dict) else v
    return simpledict