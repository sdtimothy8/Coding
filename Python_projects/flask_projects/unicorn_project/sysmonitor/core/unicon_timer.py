# -*- coding: utf-8 -*-

"""The timer manager."""

from time import time

# Global list to manage the elapsed time
last_update_times = {}


def getTimeSinceLastUpdate(IOType):
    """Return the elapsed time since last update."""
    global last_update_times
    # assert(IOType in ['net', 'disk', 'process_disk'])
    current_time = time()
    last_time = last_update_times.get(IOType)
    if not last_time:
        time_since_update = 1
    else:
        time_since_update = current_time - last_time
    last_update_times[IOType] = current_time
    return time_since_update


class Timer(object):

    """The timer class. A simple chronometer."""

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    def reset(self):
        self.start()

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time() > self.target
