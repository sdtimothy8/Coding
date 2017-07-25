# __author__ = 'root'
from util import list_result_command
from util import command_exec
# from util import trans_list_to_dict
from util import getAgentId
from util import get_dict_by_name


def get_disk_io():
    command_b = "sar -b " + "1" + " 1"
    disk_io = {}
    flag, node_id = getAgentId()
    disk_io["id"] = node_id
    disk_io["type"] = "DISK_IO"
    ret_flag, dict_list_sar_b = command_exec(command_b, 1, 1, -1, {0: "time"})
    if ret_flag:
        disk_io["body"] = dict_list_sar_b[0:-1]
        return disk_io


def get_disk_block():
    # command: sar -d 1 1
    disk_block = {}
    flag, node_id = getAgentId()
    disk_block["id"] = node_id
    command_d = "sar -d " + "1" + " 1"
    # command: iostat -xd
    command_iostat = "iostat -xd"
    ret_flag1, list_d_dict = command_exec(command_d, 1, 1, -1, {0: "time"})

    # result of command: iostat -xd
    ret_flag2, list_d2_dict = command_exec(command_iostat, 1, 1)

    # get disk name dictionary for join two result
    list_device_dict = disk_name_mapping()
    # remove average data
    list_d_dict_sub = list_d_dict[0:len(list_d_dict)/2]
    if ret_flag1 and ret_flag2:

        join_list_twocom = join_iostat_to_sard(list_d_dict_sub, list_d2_dict, list_device_dict)
        disk_block["body"] = join_list_twocom
    return disk_block


def disk_name_mapping():
        """
        return dictionary by command cat /proc/partitions
        for trans disk name
        :return:
        """
        try:
            commond_d3 = "cat /proc/partitions"
            # list = os.popen(commond_d3).readlines()
            list = list_result_command(commond_d3)
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
                line_i_con["devname"] = get_dev_name(line_i_con)
                list_d3_con.append(line_i_con)
        except:
            return None
        return list_d3_con


def join_iostat_to_sard(list_sar_d, list_iostat, disk_map):
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
            dev = sar_line["DEV"]

            # find device: from disk_map; continue when find nothing
            device_dict = get_dict_by_name("devname", dev, disk_map)
            if not device_dict or "name" not in device_dict:
                sar_line["rrqm/s"] = "0.00"
                sar_line["wrqm/s"] = "0.00"
                list_join.append(sar_line)
                continue

            device_name = device_dict["name"]
            iostat = get_dict_by_name("Device:", device_name, list_iostat)

            if not iostat or "rrqm/s" not in iostat or "wrqm/s" not in iostat:
                sar_line["rrqm/s"] = "0.00"
                sar_line["wrqm/s"] = "0.00"
                list_join.append(sar_line)
                continue

            sar_line["rrqm/s"] = iostat["rrqm/s"]
            sar_line["wrqm/s"] = iostat["wrqm/s"]
            list_join.append(sar_line)

        return list_join


def get_dev_name(line_dict):
        """
        build dev name by dict dev_major_minor
        :param line_dict:
        :return:
        """

        dev_name = ""

        if "major" in line_dict and "minor" in line_dict:
            dev_name = "dev" + line_dict["major"]\
                       + "-" + line_dict["minor"]

        return dev_name

if __name__ == "__main__":
    print get_disk_io()
