# coding=utf-8
"""
Purpose: Provide all of the classes for disk business.
"""
import os
import re

from public import functions
from diskmgr import ifconfig


class DiskBusiness():
    """
    The business class for operating disk.
    """

    def __init__(self):
        pass

    @classmethod
    def getcapacity(cls):
        """
        Get all of the disk capacity information.
        :return: boolean, dict
        For getting the physical disk information, we just launch the command as
        "lsblk".
        """
        ni_dict = {}
        ni_list = []

        ni_dict[ifconfig.DISK_KEY_LIST] = ni_list
        cmdout = functions.launchcmd(ifconfig.DISKINFO_CMDLINE)

        if cmdout:
            for line in cmdout:
                # print(line)
                matched_groups = re.match(ifconfig.DISK_INFO_PATTERN, line)
                if matched_groups:
                    # print(matched_groups.groups())
                    ni_list.append({ifconfig.DISK_KEY_NAME: matched_groups.group(1),
                                    ifconfig.DISK_KEY_CAP: matched_groups.group(2),
                                    ifconfig.DISK_KEY_TYPE: matched_groups.group(3)})
                else:
                    return False, None

        return True, ni_dict


if __name__ == "__main__":
    bflag, disk_dic = DiskBusiness.getcapacity()
    if bflag:
        print(repr(disk_dic))
