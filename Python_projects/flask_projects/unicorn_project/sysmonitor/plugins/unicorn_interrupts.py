"""
interrupts plugin.
"""
# -*- coding: utf-8 -*-

from sysmonitor.plugins.unicorn_plugin import UnicornPlugin
import sysmonitor.constant as constant

import psutil
import re
__author__ = 'yuxiubj@inspur.com'


class Plugin(UnicornPlugin):

    """ interrupts plugin.

    'stats' is a list of dictionaries that contain the interrupts infos
    for each CPU.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        UnicornPlugin.__init__(self, args=args)

        # We want to display the stat in the curse interface
        self.display_curse = True

        self._cpu_number = psutil.cpu_count()

        # Init stats
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return constant.DICT_KEYS_CPU_NUMBER

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def update(self, cpunumbers, cpu_num):
        """Update interrupts stats using the input method."""
        # Reset stats
        self.reset()

        # return the information in /proc/interrupts
        with open("/proc/interrupts") as intrf:
            intnum = 0
            for line in intrf:
                if line.strip():
                    deal_line = self.deal_with_line(cpunumbers, line)
                    if(intnum == 0):
                        deal_line.insert(0, constant.SPACE_BLANK)
                    intnum += 1
                    self.stats.append(deal_line)
        if constant.URL_PARAM_CPUNUM_DEFAULT == cpu_num:
            return self.stats
        else:
            stats_cpu_num = self.cutline_by_cpunum(cpu_num)
            return stats_cpu_num

    def cutline_by_cpunum(self, cpu_num):
        """
        get the interruptes of cpu[cpu_num]
        :param cpu_num:
        :return:
        """
        stats_cpu_num = []
        # get the max length of self.stats.list
        max_length = 0
        for line in self.stats:
            if len(line) > max_length:
                max_length = len(line)

        for line in self.stats:
            line_cpu_num = []
            line_cpu_num.append(line[0])
            if len(line) >= cpu_num+2:
                line_cpu_num.append(line[cpu_num+1])
            if len(line) >= max_length-1:
                line_cpu_num.append(line[max_length-2])
            if len(line) >= max_length:
                line_cpu_num.append(line[max_length-1])
            stats_cpu_num.append(line_cpu_num)
        return stats_cpu_num

    def deal_with_line(self, cpunumbers, line):
        """
        split line of cmd with "  +",
        and split 0-cpunumbers of list with " "
        :param cpunumbers:
        :param line:
        :return:
        """
        linelist = re.sub(constant.RE_SEPARATOR, constant.JOINER_SPECIAL, line.strip()).split(constant.JOINER_SPECIAL)
        l_index = 0
        for line_str in linelist:
            # break when linelist[l_index] is None or l_index is bigger than cpunumbers
            # split linelist[l_index] when there is space in the string
            # then insert the split list into linelist
            if len(linelist) <= l_index or l_index > cpunumbers:
                break
            elif linelist[l_index] \
                    and linelist[l_index].find(" ") > -1 \
                    and re.match(r"^[\d ]+$|\w+:[\d ]+", linelist[l_index]):
                new_list = linelist[l_index].strip().split()
                teal_list = linelist[l_index+1:]
                linelist = linelist[0:l_index]
                linelist.extend(new_list)
                linelist.extend(teal_list)
                l_index = l_index + len(new_list) - 1
            l_index = l_index + 1

        return linelist
