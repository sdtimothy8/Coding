# -*- coding: utf-8 -*-

"""process system file plugin."""

from sysmonitor.plugins.unicorn_plugin import UnicornPlugin
from sysmonitor.common import Common
__author__ = 'yuxiubj@inspur.com'


class Plugin(UnicornPlugin):

    """ system file  io plugin.

    'stats' is a list of dictionaries
    """

    def __init__(self, args=None):
        """
        Init the plugin.
        """
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        # Init stats
        self.reset()

    def reset(self):
        """
        Reset/init the stats.
        """
        self.stats = []

    def update(self):
        """
        Update stats using the input method.
        :return:
        """

        # Reset stats
        self.reset()
        # command: df -h
        command = "df -h"
        try:
            ret_flag, list_df = Common.command_exec(command, 0)
            if ret_flag:
                list_df[0] = "device_name  size  used  free  percent  mnt_point"
                dict_list_df = Common.trans_list_to_dict(list_df)
                return dict_list_df
            else:
                return list_df
        except:
            return None
