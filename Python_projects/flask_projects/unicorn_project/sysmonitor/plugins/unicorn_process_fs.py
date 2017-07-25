# -*- coding: utf-8 -*-

"""process open file (lsof) plugin."""

from sysmonitor.plugins.unicorn_plugin import UnicornPlugin

import os
__author__ = 'yuxiubj@inspur.com'


class Plugin(UnicornPlugin):

    """ process open file plugin.

    'stats' is a list of dictionaries that contain lsof infos
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init stats
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def update(self, pro_pid):
        """Update stats using the input method."""
        # Reset stats
        self.reset()

        if not pro_pid:
            return self.stats

        command = "lsof -p " + str(pro_pid)
        for line in os.popen(command).readlines():
            self.stats.append(line.strip())

        return self.stats
