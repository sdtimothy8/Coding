# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#
import logging

from .connection import vmmConnection

class vmmEngine(object):
    def __init__(self):
        self.conns = {}

    def start(self, uri="", show_window="", domain="", skip_autostart=False):
        tryuri = "qemu:///system"
        connected = self.open(tryuri)
        if not connected:
            logging.error("The 'libvirtd' service will need to be started")

    def open(self, uri):
        conn = self._make_conn(uri)
        conn.open()
        return conn
        
    def get_conn(self, uri):
        return self._check_conn(uri)

    def _check_conn(self, uri):
        conn = self.conns.get(uri)
        if conn:
            return conn["conn"]
        return None

    def _make_conn(self, uri):
        conn = self._check_conn(uri)
        if conn:
            return conn
        conn = vmmConnection(uri)
        self.conns[uri] = {
            "conn": conn,
        }
        return conn

    def _cleanup(self):
        for uri in self.conns:
            self.cleanup_conn(uri)
        self.conns = {}

    def cleanup_conn(self, uri):
        try:
            self.conns[uri]["conn"]._cleanup()
        except Exception,e:
            logging.exception("Error cleaning up conn in engine")