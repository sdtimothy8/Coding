# __author__ = 'caofengbing'
import commands
from util import command_exec, getAgentId


def get_fans():

    (code, resultMSG) = commands.getstatusoutput('ipmitool -I open sensor list')
    #  temp_fans = {"id": "node1", "fans": [{"fanname": "fan1", "fanspeed": "3000"},
    # {"fanname": "fan2", "fanspeed": "3000"}]}
    error = {}
    error["type"] = "ERROR"
    if code != 0:
        error["error"] = resultMSG
        return error
    fanlist = {"fans": []}
    flag, node_id = getAgentId()
    fanlist["id"] = node_id
    fanlist["type"] = "FANS"
    line = resultMSG.split('\n')
    for i in range(len(line)):
        tmp = line[i].split('|')
        tmpdict = {}
        date = tmp[0]
        if date.find('FAN') != -1:
            tmpdict['fanname'] = tmp[0].strip()
            tmpdict['fanspeed'] = tmp[1].strip()
            fanlist['fans'].append(tmpdict)
    return fanlist


def get_sensor():
    """
    get sensors.
    :return:
    """
    stats = []
    command = "sensors"
    try:
        ret_flag, list_sensors = command_exec(command, 0)
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
                        stats.append(line_con)
            return stats
        else:
            return list_sensors
    except:
        return None


def deal_cpu_sensor():
    """
    get dict that label contains Core or physical id
    :return:
    """
    re_list = []
    cpu = {}
    flag, node_id = getAgentId()
    cpu["id"] = node_id
    # core_index = 0
    list_sensor = get_sensor()
    for r_dict in list_sensor:
        if r_dict["label"] is not None \
                and (r_dict["label"].find("Physical id ") != -1 or r_dict["label"].find("Core ") != -1):
            re_list.append(r_dict)
    cpu["body"] = re_list
    return cpu

if __name__ == "__main__":

    print deal_cpu_sensor()
