# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

"""
VMManager,instance of virtlib.Manager
    manage vm(-related) transaction
    such as Connection, VM Event, VM Config...
    goto virtlib/manager.py for more details

VMConn, instance of virtlib.Connection
    this "VMConn" object only manage *default* connection
    between vmmanager and host(which running this vmmanager) directly
    goto virtlib/connection.py for more details

DEFAULT_URI, *default* connection's uri
"""
from virtlib.manager import Manager as BackgroundManager

# BackgroundManager instance, auto start vm manager deamon task
# such as data collection, status collection, event listener...
VMManager = BackgroundManager()

DEFAULT_URI = "qemu:///system"


def _default_conn():
    """
    Makesure background api return *active* connection
    """
    try:
        VMManager._cleanup()
    except Exception, e:
        raise
    VMManager.open(DEFAULT_URI)
    conn = VMManager.get_conn(DEFAULT_URI)
    return conn
# Default vm manager deamon connection.
get_conn = _default_conn
