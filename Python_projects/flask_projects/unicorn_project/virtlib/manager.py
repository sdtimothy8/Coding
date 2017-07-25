# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

def _make_virt_env():
    from .engine import vmmEngine
    engine = vmmEngine()
    return engine
    
class Manager(object):
    def __init__(self):
        self._engine = _make_virt_env()
    
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        # Proxy API calls
        engine = self.__dict__.get("_engine")
        return getattr(engine, attr)