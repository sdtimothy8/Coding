# -*- coding: utf-8 -*-

"""CPU percent stats shared between CPU and Quicklook plugins."""

from sysmonitor.core.unicon_timer import Timer

import psutil


class CpuPercent(object):

    """Get and store the CPU percent."""

    def __init__(self, cached_time=1):
        self.cpu_percent = 0

        # cached_time is the minimum time interval between stats updates
        # since last update is passed (will retrieve old cached info instead)
        self.timer = Timer(0)
        self.cached_time = cached_time

    def get(self):
        """Update and/or return the CPU using the psutil library."""
        # Never update more than 1 time per cached_time
        if self.timer.finished():
            self.cpu_percent = psutil.cpu_percent(interval=0.0)
            self.timer = Timer(self.cached_time)
        return self.cpu_percent


# CpuPercent instance shared between plugins
cpu_percent = CpuPercent()
