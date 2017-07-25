from util import command_exec, trans_list_to_dict, getAgentId


def getfs():
    command = "df -h"
    flag, node_id = getAgentId()
    file = {}
    result = []
    file["id"] = node_id
    try:
        ret_flag, list_df = command_exec(command, 0)
        if ret_flag:
            list_df[0] = "devicename  size  used  free  percent  mntpoint"
            dict_list_df = trans_list_to_dict(list_df)
            for data in dict_list_df:
                if data['devicename'] != 'tmpfs':
                    result.append(data)
            file["body"] = result
            return file
        else:
            file["body"] = list_df
            return file
    except:
        return None

if __name__ == "__main__":
    print getfs()
