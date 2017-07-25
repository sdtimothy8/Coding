"""
Purpose: Provide all of the method for ft module.
"""

import sys
import ksmp.logger as log
import sysmonitor.constant as constant
from sysmonitor.plugins.unicorn_fs import Plugin as plugin_fs
from sysmonitor.plugins.unicorn_sysfs import Plugin as plugin_sysfs

reload(sys)
sys.setdefaultencoding("utf-8")
__author__ = 'yuxiubj@inspur.com'


class Servicefs():
    """
    The business class for operating logList.
    """

    def __init__(self):
        """
        init
        :return:
        """
        self._plugin_fs = plugin_fs()
        # self._plugin_pro_fs = plugin_pro_fs()
        self._plugin_sysfs = plugin_sysfs()

        # Init stats
        self.reset()

    def update_stats(self, request, itemid):
        """
        update data
        :param request:
        :param itemid:
        :return:
        """
        log.debug(constant.LOG_START_SYSFILE + itemid)
        if constant.SYSFILE_BASIC_URL == itemid:
            stats_sysfs = self._plugin_sysfs.update()
            log.debug(constant.LOG_END_SYSFILE)
            if stats_sysfs is not None:
                return True, stats_sysfs
            else:
                return False, "can not get data."
        elif "glances" == itemid:
            stats_fs = self._plugin_fs.update()
            log.debug(constant.LOG_END_SYSFILE)
            return True, stats_fs
        else:
            log.error(constant.EXCEPT_URL_ERROR + itemid)
            return False, constant.EXCEPT_URL_ERROR

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

fsmonitor = Servicefs()
