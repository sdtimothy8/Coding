"""
This module provide classes for monitor Memory info
"""
import os
import psutil
from string import strip
from string import lower
from public import functions
from ksmp import logger

__author__ = 'zhuysh@inspur.com'


class MemBusiness():
    """
    this class provides methods for memory monitor
    """

    @classmethod
    def get_mem_info(cls, keys):
        """
        get memory info
        :param keys: the items
        :return:
        """

        virtual_memory = {}

        try:
            freem = functions.launchcmd('free').readlines()
            shared = int(strip(freem[1].split()[4])) * 1024
            rtinfo = psutil.virtual_memory()
            if rtinfo:
                rtinfo_list = str(rtinfo).replace("svmem(", "").replace(")", "").split(",")
                for item in rtinfo_list:
                    items = item.split("=")

                    if "all" in keys or [] == keys:
                        virtual_memory[strip(items[0])] = strip(items[1])
                    elif strip(items[0]) in keys:
                        virtual_memory[strip(items[0])] = strip(items[1])

            if "all" in keys or "shared" in keys or [] == keys:
                virtual_memory["shared"] = shared

        except IOError:
            return False, virtual_memory

        return True, virtual_memory

    @classmethod
    def get_swap_info(cls, keys):
        """
        get swap info
        :param keys: the items
        :return:
        """

        swap_memory = {}

        try:
            rtinfo = psutil.swap_memory()
            if rtinfo:
                logger.debug("--------get swap memory info begin-------")
                rtinfo_list = str(rtinfo).replace("sswap(", "").replace(")", "").split(",")
                pg_in_out = functions.launchcmd('sar -W 1 1').readlines()
                logger.debug("cmd:sar -W 1 1 finished")
                for item in rtinfo_list:
                    items = item.split("=")
                    if ("all" in keys or [] == keys) and strip(items[0]) in ("total", "used", "free"):
                        swap_memory[strip(items[0])] = strip(items[1])
                    elif strip(items[0]) in keys:
                        swap_memory[strip(items[0])] = strip(items[1])

                if "all" in keys or [] == keys:
                    swap_memory["pswpin"] = pg_in_out[-1].split()[1]
                    swap_memory["pswpout"] = pg_in_out[-1].split()[2]

                for key in keys:
                    if key == "pswpin":
                        swap_memory["pswpin"] = pg_in_out[-1].split()[1]
                    elif key == "pswpout":
                        swap_memory["pswpout"] = pg_in_out[-1].split()[2]

        except IOError:
            return False, swap_memory

        return True, swap_memory

    @classmethod
    def get_page_info(cls, keys):
        """
        get page info
        :param keys: the items
        :return:
        """

        page_memory = {}
        rtn_page_memory = {}

        try:
            rtinfo = functions.launchcmd('sar -B 1 1').readlines()
            if rtinfo[-1]:
                page_list = rtinfo[-1].split()
                page_memory["pgpgin"] = page_list[1]
                page_memory["pgpgout"] = page_list[2]
                page_memory["fault"] = page_list[3]
                page_memory["majflt"] = page_list[4]
                page_memory["pgfree"] = page_list[5]
                page_memory["pgsteal"] = page_list[8]

            rtinfo_other = functions.launchcmd('sar -R 1 1').readlines()
            if rtinfo_other[-1]:
                page_list_other = rtinfo_other[-1].split()
                page_memory["bufpg"] = page_list_other[2]
                page_memory["campg"] = page_list_other[3]

            if "all" in keys or [] == keys:
                return True, page_memory
            else:
                for key in keys:
                    rtn_page_memory[key] = page_memory[key]
                return True, rtn_page_memory

        except IOError:
            return False, page_memory

        return True, page_memory

    @classmethod
    def get_slab_info(cls, name, keys):
        """
        get slab info
        :param keys: the items
        :return:
        """

        slab_list = []

        try:
            logger.debug("slabtop begin:======>")
            rtinfo = functions.launchcmd('slabtop -o').readlines()
            logger.debug("commands finished! length=")
            logger.debug(len(rtinfo))
            if rtinfo:
                continue_falg = True
                if "" == name:
                    for item in rtinfo:
                        slab_info = {}
                        if continue_falg:
                            if "OBJS" in item:
                                continue_falg = False
                            continue
                        slab_info["name"] = item.split()[7]
                        slab_info["objs"] = item.split()[0]
                        slab_info["slabs"] = item.split()[4]
                        slab_info["obj_slab"] = item.split()[5]
                        slab_info["active"] = item.split()[1]
                        slab_info["obj_size"] = item.split()[3]
                        slab_info["use"] = item.split()[2]
                        slab_list.append(slab_info)
                    return True, slab_list
                else:
                    slab_info = {}
                    slab_info_temp = {}
                    for item in rtinfo[7:]:

                        if name == item.split()[7]:
                            slab_info_temp["name"] = item.split()[7]
                            slab_info_temp["objs"] = item.split()[0]
                            slab_info_temp["slabs"] = item.split()[4]
                            slab_info_temp["obj_slab"] = item.split()[5]
                            slab_info_temp["active"] = item.split()[1]
                            slab_info_temp["obj_size"] = item.split()[3]
                            slab_info_temp["use"] = item.split()[2]
                            break
                    if "all" in keys:
                        slab_list.append(slab_info_temp)
                        return True, slab_info_temp
                    for key in keys:
                        slab_info[key] = slab_info_temp[key]

                    return True, slab_info

        except IOError:
            return False, slab_list

        return True, slab_list

    @classmethod
    def get_numastat_info(cls):
        """
        get numastat info
        :return:
        """

        numastat_list = []
        numastat = []

        try:
            rtninfo = functions.launchcmd('numastat').readlines()

            for item in rtninfo:
                items = item.split()
                numastat.append(items)
            logger.debug(numastat)
            logger.debug(len(numastat[0]))
            for i in range(0, len(numastat[0])):
                numastat_info = {}
                logger.debug(i)
                numastat_info["name"] = numastat[0][i]
                numastat_info["numa_hit"] = numastat[1][i + 1]
                numastat_info["numa_miss"] = numastat[2][i + 1]
                numastat_info["numa_foreign"] = numastat[3][i + 1]
                numastat_info["interleave_hit"] = numastat[4][i + 1]
                numastat_info["local_node"] = numastat[5][i + 1]
                numastat_info["other_node"] = numastat[6][i + 1]
                numastat_list.append(numastat_info)

            # numastat_info["numastat_list"] = numastat_list
        except IOError:
            return False, numastat_list

        return True, numastat_list
