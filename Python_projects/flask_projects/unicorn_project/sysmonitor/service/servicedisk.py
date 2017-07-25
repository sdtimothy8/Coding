"""
Purpose: Provide all of the method for disk module.
"""

import sys
import ksmp.logger as log
import sysmonitor.constant as constant
from sysmonitor.plugins.unicorn_disk_com import Plugin as plugin_sar

reload(sys)
sys.setdefaultencoding("utf-8")
__author__ = 'yuxiubj@inspur.com'


class Servicedisk():
    """
    The business class for operating logList.
    """

    def __init__(self):
        """
        init
        :return:
        """
        self._plugin_sar = plugin_sar()

        # Init stats
        self.reset()

    def update_stats(self, request, itemid):
        """
        update data
        :param request:
        :param itemid:
        :return:
        """
        log.info(constant.LOG_START_DISK + itemid)
        self.stats = self._plugin_sar.update(itemid)
        if not self.stats:
            log.info(constant.EXCEPT_RESULT_NONE + itemid)
            return False, constant.EXCEPT_RESULT_NONE
        log.info(constant.LOG_END_DISK)
        return True, self.stats

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

diskmonitor = Servicedisk()
