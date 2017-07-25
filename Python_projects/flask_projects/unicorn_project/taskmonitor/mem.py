# __author__ = 'root'
from util import launchcmd
from string import strip
import psutil
from util import getAgentId


def getmembasicinfo():
    """
    get memory info
    :param
    :return:
    """
    virtual_memory = {}
    flag, node_id = getAgentId()
    virtual_memory["id"] = node_id
    try:
        freem = launchcmd('free').readlines()
        shared = int(strip(freem[1].split()[4])) * 1024
        rtinfo = psutil.virtual_memory()
        if rtinfo:
            rtinfo_list = str(rtinfo).replace("svmem(", "").replace(")", "").split(",")
            for item in rtinfo_list:
                items = item.split("=")
                virtual_memory[strip(items[0])] = strip(items[1])
            virtual_memory["shared"] = shared

    except IOError:
        return virtual_memory

    return virtual_memory


def getpaginfo():
    """
    get mem pag info
    :return:
    """

    page_memory = {}
    flag, node_id = getAgentId()
    page_memory["id"] = node_id
    try:
        rtinfo = launchcmd('sar -B 1 1').readlines()
        if rtinfo[-1]:
            page_list = rtinfo[-1].split()
            page_memory["pgpgin"] = page_list[1]
            page_memory["pgpgout"] = page_list[2]
            page_memory["fault"] = page_list[3]
            page_memory["majflt"] = page_list[4]
            page_memory["pgfree"] = page_list[5]
            page_memory["pgsteal"] = page_list[8]
        rtinfo_other = launchcmd('sar -R 1 1').readlines()
        if rtinfo_other[-1]:
            page_list_other = rtinfo_other[-1].split()
            page_memory["bufpg"] = page_list_other[2]
            page_memory["campg"] = page_list_other[3]

    except IOError:
        return page_memory
    return page_memory


def get_swap_info():
    """
    get swap info
    :param
    :return:
    """
    swap_memory = {}
    flag, node_id = getAgentId()
    swap_memory["id"] = node_id
    try:
        rtinfo = psutil.swap_memory()
        if rtinfo:
            rtinfo_list = str(rtinfo).replace("sswap(", "").replace(")", "").split(",")
            pg_in_out = launchcmd('sar -W 1 1').readlines()
            for item in rtinfo_list:
                items = item.split("=")
                swap_memory[strip(items[0])] = strip(items[1])
                swap_memory["pswpin"] = pg_in_out[-1].split()[1]
                swap_memory["pswpout"] = pg_in_out[-1].split()[2]
    except IOError:
        return swap_memory

    return swap_memory


def get_slab_info():
        """
        get slab info
        :return:
        """

        slab_list = []
        slab_res = {}
        flag, node_id = getAgentId()
        slab_res["id"] = node_id

        try:
            rtinfo = launchcmd('slabtop -o').readlines()
            if rtinfo:
                continue_falg = True
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
                slab_res["body"] = slab_list
                return slab_res

        except IOError:
            return slab_res

        return slab_res


def get_numastat_info():
        """
        get numastat info
        :return:
        """

        numastat_list = []
        numastat = []
        numa_dict = {}
        flag, node_id = getAgentId()
        numa_dict["id"] = node_id

        try:
            rtninfo = launchcmd('numastat').readlines()
            for item in rtninfo:
                items = item.split()
                numastat.append(items)
            for i in range(0, len(numastat[0])):
                numastat_info = {}
                numastat_info["name"] = numastat[0][i]
                numastat_info["numa_hit"] = numastat[1][i + 1]
                numastat_info["numa_miss"] = numastat[2][i + 1]
                numastat_info["numa_foreign"] = numastat[3][i + 1]
                numastat_info["interleave_hit"] = numastat[4][i + 1]
                numastat_info["local_node"] = numastat[5][i + 1]
                numastat_info["other_node"] = numastat[6][i + 1]
                numastat_list.append(numastat_info)
            numa_dict["body"] = numastat_list
        except IOError:
            return numa_dict

        return numa_dict


def get_total_memory():
    """
    get total memory info from system.
    :return:
    """
    result = {}
    result["membasic"] = getmembasicinfo()
    result["memswap"] = get_swap_info()
    result["memslab"] = get_slab_info()
    result["mempage"] = getpaginfo()
    result["type"] = "MEM_INFO"
    return result

if __name__ == "__main__":

    print getindexmembasicinfo()
