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
        command = "sensors"
        try:
            ret_flag, list_sensors = Common.command_exec(command, 0)
            if ret_flag:
                for line in list_sensors:
                    if (line.strip().find("Physical ") >= 0 or line.strip().find("Core ") >= 0) \
                            and line.strip().find("(") >= 0 \
                            and line.strip().find(":") >= 0:
                        l_index = line.strip().find("(")
                        line = line.strip()[0:l_index]
                        line_list = line.strip().split(":")
                        if line_list is not None \
                                and len(line_list) > 1 \
                                and line_list[0] is not None \
                                and line_list[1] is not None:
                            plus_pos = line_list[1].strip().find("+")
                            doc_pos = line_list[1].strip().find(".")
                            lable_c = line_list[0].strip()
                            value_c = "0"
                            if doc_pos >= 0 and 0 <= plus_pos < doc_pos:
                                value_c = line_list[1].strip()[plus_pos+1:doc_pos+2]
                            line_con = {"label": lable_c,
                                        "value": value_c}
                            self.stats.append(line_con)
                return self.stats
            else:
                return list_sensors
        except:
            return None
