from util import command_exec
import psutil


def get_ps_disk_info():

    disk_ps_info = {}
    command = "iotop -P -b -n 1 | head -n 4"
    try:
        ret_flag, net_info_list = command_exec(command, 0)
        disk_ps_info["psdiskinfo"] = net_info_list[-1].split()[0]
        if disk_ps_info["psdiskinfo"].isdigit() and psutil.pid_exists(int(disk_ps_info["psdiskinfo"])):
            disk_ps_info["io"] = (float)(net_info_list[-1].split()[9])
            disk_ps_info["name"] = psutil.Process(int(disk_ps_info["psdiskinfo"])).name()
            return disk_ps_info
        else:
            disk_ps_info["name"] = ""
            return disk_ps_info
    except:
        return None

if __name__ == "__main__":
    print get_ps_disk_info()
