"""
Purpose: Provide all of the method for cpu module.
"""

import sys
import ksmp.logger as log
import sysmonitor.constant as constant
from sysmonitor.plugins.unicorn_cpu import Plugin as plugin_cpu
from sysmonitor.plugins.unicorn_percpu import Plugin as plugin_per_cpu
from sysmonitor.plugins.unicorn_load import Plugin as plugin_load
from sysmonitor.plugins.unicorn_interrupts import Plugin as plugin_interrupts
from sysmonitor.plugins.unicorn_cmd_sensor import Plugin as plugin_sensors
from sysmonitor.common import Common
from public import functions

reload(sys)
sys.setdefaultencoding("utf-8")
__author__ = 'yuxiubj@inspur.com'


class Servicecpu():
    """
    The business class for operating logList.
    """

    def __init__(self):
        """
        init cpu service
        :return:
        """
        self._plugin_cpu = plugin_cpu()
        self._plugin_load = plugin_load()
        self._plugin_per_cpu = plugin_per_cpu()
        self._plugin_interrupts = plugin_interrupts()
        self._plugin_sensors = plugin_sensors()

        # Init stats
        self.reset()

    def update_stats(self, request, itemid):
        """
        intface of get cpu info
        :param request:
        :param itemid: which info to return
        :return:
        """

        self.reset()
        # get cpu core numbers
        stats_load = self._plugin_load.update()
        cpunumbers = self.get_core_num()

        # get cpu num param , "all" for default
        if request.GET.get(constant.URL_PARAM_CPUNUM):
            cpuNum = int(request.GET[constant.URL_PARAM_CPUNUM])  # 0,1,2,3
            if cpunumbers <= cpuNum or cpuNum < 0:
                return False, constant.EXCEPT_URL_PARAM_ERROR
        else:
            cpuNum = constant.URL_PARAM_CPUNUM_DEFAULT

        log.info(constant.LOG_START_CPU + itemid)
        # get load | baseinfo | interrupts | perinfo | all | sensor info by apply
        if constant.CPU_LOAD_URL == itemid:
            log.info(constant.LOG_END_CPU)
            return True, stats_load
        elif constant.CPU_BASEINFO_URL == itemid:
            stats_cpu = self._plugin_cpu.update()
            log.info(constant.LOG_END_CPU)
            return True, stats_cpu
        elif constant.CPU_INTERRUPTS_URL == itemid:
            stats_interrupts = self._plugin_interrupts.update(cpunumbers, cpuNum)
            log.info(constant.LOG_END_CPU)
            return True, stats_interrupts
        elif constant.CPU_PERINFO_URL == itemid or constant.CPU_ALL_URL == itemid:
            stats_per_cpu = self._plugin_per_cpu.update()
            if constant.CPU_ALL_URL == itemid:
                log.info(constant.LOG_END_CPU)
                return True, stats_per_cpu
            stats_per_cpu_num = self.get_cpuinfo_num(cpuNum, stats_per_cpu)
            log.info(constant.LOG_END_CPU)
            return True, stats_per_cpu_num
        elif constant.CPU_SENSOR_URL == itemid or constant.CPU_PERSENSOR_URL == itemid:
            stats_sen = self.deal_cpu_sensor(self._plugin_sensors.update())
            if constant.CPU_SENSOR_URL == itemid:
                log.info(constant.LOG_END_CPU)
                return True, stats_sen
            else:
                reflag, per_sensor = self.get_percpu_sensor(stats_sen, request)
                log.info("get per cpu sensor by physical id.")
                log.info(constant.LOG_END_CPU)
                return reflag, per_sensor
        else:
            log.info(constant.EXCEPT_URL_ERROR + itemid)
            return False, constant.EXCEPT_URL_ERROR

    def reset(self):
        """
        Reset/init the stats.
        :return:
        """
        self.stats = []

    def deal_cpu_sensor(self, list_sensor):
        """
        get dict that label contains Core or physical id
        :param list_sensor:
        :return:
        """
        re_list = []
        core_index = 0
        for r_dict in list_sensor:
            if r_dict["label"] is not None \
                    and (r_dict["label"].find("Physical id ") != -1 or r_dict["label"].find("Core ") != -1):
                re_list.append(r_dict)
        return re_list

    def get_percpu_sensor(self, list_sensor, request):
        """
        get physical sensor when only have param phyId
        get core sensor when have phyId and coreId
        :param list_sensor:
        :param request:
        :return:
        """
        if request.GET.get(constant.URL_PARAM_PHYID):
            physicalNum = int(request.GET[constant.URL_PARAM_PHYID])
        else:
            return False, "error physical number, physical number like 0,1,2,3"

        # get physical temper
        physical_str = "Physical id " + str(physicalNum)
        if not request.GET.get(constant.URL_PARAM_COREID):
            physical_dict = Common.get_dict_by_name("label", physical_str, list_sensor)
            if physical_dict is not None:
                return True, physical_dict
            else:
                return False, "no data by " + physical_str

        # get core temper
        coreNum = int(request.GET[constant.URL_PARAM_COREID])
        core_str = "Core " + str(coreNum)
        physical_index = Common.get_index_by_name("label", physical_str, list_sensor)
        if physical_index == -1:
            return False, "no data find by " + physical_str

        list_part_sensor = list_sensor[physical_index:]
        for map in list_part_sensor:
            if map["label"].find("Physical id ") >= 0 \
                    and map["label"] != physical_str:
                return False, "no data find by " + physical_str + " Core: " + core_str
            if map["label"] == core_str:
                return True, map
        return False, "no data find by " + physical_str + " Core: " + core_str

    def get_cpuinfo_num(self, cpuNum, list_cpu):
        """
        get cpuinfo by num
        :param cpuNum:
        :param list_cpu:
        :return:
        """
        try:
            stats_per_cpu_num = Common.get_dict_by_name(constant.DICT_KEYS_CPU_NUMBER, cpuNum, list_cpu)
            if stats_per_cpu_num is None:
                return constant.EXCEPT_RESULT_NONE + cpuNum
            return stats_per_cpu_num
        except:
            return constant.EXCEPT_DEFAULT

    def get_core_num(self):
        # CPU core num
        proc_cpu_cores = functions.launchcmd('cat /proc/cpuinfo | grep "processor" |wc -l').readline()
        return proc_cpu_cores

cpumonitor = Servicecpu()
