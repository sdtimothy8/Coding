# -*- coding: utf-8 -*-

"""process diskio plugin."""

from sysmonitor.plugins.unicorn_plugin import UnicornPlugin
from sysmonitor.common import Common
import sysmonitor.constant as constant
__author__ = 'yuxiubj@inspur.com'


class Plugin(UnicornPlugin):

    """ disk io plugin.

    'stats' is a list of dictionaries that contain sar infos
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

    def update(self, data_type="all", interval=1):
        """
        Update stats using the input method.
        :param data_type:
        :param interval:
        :return:
        """

        # Reset stats
        self.reset()
        # command: sar -b 1 1
        command_b = "sar -b " + str(interval) + " 1"
        # command: sar -d 1 1
        command_d = "sar -d " + str(interval) + " 1"
        # command: iostat -xd
        command_iostat = "iostat -xd"

        try:
            if constant.DISK_IO_URL == data_type:
                # result of command: sar -b 1 1
                ret_flag, dict_list_sar_b = Common.command_exec(command_b, 1, 1, -1, {0: constant.DICT_KEYS_TIME})
                if ret_flag:
                    return dict_list_sar_b[0:-1]
            elif constant.DISK_BLOCK_URL == data_type:
                # result of command: sar -d 1 1
                ret_flag1, list_d_dict = Common.command_exec(command_d, 1, 1, -1, {0: constant.DICT_KEYS_TIME})

                # result of command: iostat -xd
                ret_flag2, list_d2_dict = Common.command_exec(command_iostat, 1, 1)

                # get disk name dictionary for join two result
                list_device_dict = self.disk_name_mapping()

                # remove average data
                list_d_dict_sub = list_d_dict[0:len(list_d_dict)/2]
                if ret_flag1 and ret_flag2:
                    # join sar -d and iostat result
                    join_list_twocom = self.join_iostat_to_sard(list_d_dict_sub, list_d2_dict, list_device_dict)
                    return join_list_twocom
            else:
                return self.stats
        except:
            return None

    def join_iostat_to_sard(self, list_sar_d, list_iostat, disk_map):
        """
        join list_iostat to list_sar_d
        disk_map:translate DEV to Device
        :param list_sar_d:
        :param list_iostat:
        :param disk_map:
        :return:
        """
        list_join = []
        for sar_line in list_sar_d:
            dev = sar_line[constant.DICT_KEYS_DEV]

            # find device: from disk_map; continue when find nothing
            device_dict = Common.get_dict_by_name(constant.DICT_KEYS_DEVNAME, dev, disk_map)
            if not device_dict or constant.DICT_KEYS_NAME not in device_dict:
                sar_line[constant.DICT_KEYS_RRQM] = "0.00"
                sar_line[constant.DICT_KEYS_WRQM] = "0.00"
                list_join.append(sar_line)
                continue

            device_name = device_dict[constant.DICT_KEYS_NAME]
            iostat = Common.get_dict_by_name(constant.DICT_KEYS_DEVICE, device_name, list_iostat)

            if not iostat or constant.DICT_KEYS_RRQM not in iostat or constant.DICT_KEYS_WRQM not in iostat:
                sar_line[constant.DICT_KEYS_RRQM] = "0.00"
                sar_line[constant.DICT_KEYS_WRQM] = "0.00"
                list_join.append(sar_line)
                continue

            sar_line[constant.DICT_KEYS_RRQM] = iostat[constant.DICT_KEYS_RRQM]
            sar_line[constant.DICT_KEYS_WRQM] = iostat[constant.DICT_KEYS_WRQM]
            list_join.append(sar_line)

        return list_join

    def disk_name_mapping(self):
        """
        return dictionary by command cat /proc/partitions
        for trans disk name
        :return:
        """
        try:
            commond_d3 = "cat /proc/partitions"
            # list = os.popen(commond_d3).readlines()
            list = Common.list_result_command(commond_d3)
            length_list = len(list)
            line_0 = list[0].strip().split()
            length_line = len(line_0)
            list_d3_con = []
            for i in range(1, length_list):
                if len(list[i].strip()) == 0:
                    continue
                line_i = list[i].strip().split()
                line_i_con = {}
                for j in range(0, length_line):
                    line_i_con[line_0[j]] = line_i[j]
                line_i_con[constant.DICT_KEYS_DEVNAME] = self.get_dev_name(line_i_con)
                list_d3_con.append(line_i_con)
        except:
            return None
        return list_d3_con

    def get_dev_name(self, line_dict):
        """
        build dev name by dict dev_major_minor
        :param line_dict:
        :return:
        """

        dev_name = ""
        if constant.DICT_KEYS_MAJOR in line_dict and constant.DICT_KEYS_MINOR in line_dict:
            dev_name = constant.DICT_KEYS_DEV_STR + line_dict[constant.DICT_KEYS_MAJOR]\
                       + constant.JOINER + line_dict[constant.DICT_KEYS_MINOR]
        return dev_name
