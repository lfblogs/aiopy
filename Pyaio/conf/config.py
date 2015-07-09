#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 3.4.x
# Last Modified: 2015/7/8 21:22


__all__ = []
__author__ = "lfblogs (email:13701242710@163.com)"
__version__ = "1.0.1"

from Pyaio.conf.method import ProduceDict, MergeDict, Configure2Dict

def Configure(configs, configs_prodution = None):
    if configs_prodution:
        config = ProduceDict(MergeDict(Configure2Dict(configs),Configure2Dict(configs_prodution)))
    else:
        config = ProduceDict(Configure2Dict(configs))
    return config
