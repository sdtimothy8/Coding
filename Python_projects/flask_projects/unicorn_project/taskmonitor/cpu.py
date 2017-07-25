import os
import sys
import psutil
import re
import subprocess
from util import launchcmd, getAgentId
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ksmp.settings'

from sysmonitor.service.servicecpu import cpumonitor

def getcpuload():
    flag, node_id = getAgentId()
    try:
        load = os.getloadavg()
    except (OSError, AttributeError):
        stats = {}
    else:
        stats = {'min1': load[0],
                 'min5': load[1],
                 'min15': load[2],
                 'id': node_id
                 }
        return stats


def getcpuinfo():
    stats = {}
    flag, node_id = getAgentId()
    stats["id"] = node_id
    stats["total"] = psutil.cpu_percent(interval=0.0)
    cpu_times_percent = psutil.cpu_times_percent(interval=0.0)
    for stat in ['user', 'system', 'idle', 'nice', 'iowait',
                         'irq', 'softirq', 'steal', 'guest', 'guest_nice']:
        if hasattr(cpu_times_percent, stat):
            stats[stat] = getattr(cpu_times_percent, stat)
    return stats


def getinterrupts():
    intnum = 0
    stats = []
    interrupts = {}
    flag, node_id = getAgentId()
    interrupts["id"] = node_id
    cpunumbers = get_core_num()
    with open("/proc/interrupts") as intrf:
        intnum = 0
        for line in intrf:
            if line.strip():
                deal_line = deal_with_line(cpunumbers, line)
                if(intnum == 0):
                    deal_line.insert(0, " ")
                intnum += 1
                stats.append(deal_line)
        interrupts["body"] = stats
        return interrupts


def deal_with_line(cpunumbers, line):
    """
    split line of cmd with "  +",
    and split 0-cpunumbers of list with " "
    :param cpunumbers:
    :param line:
    :return:
    """
    linelist = re.sub("  +", "&@", line.strip()).split("&@")
    l_index = 0
    for line_str in linelist:
        # break when linelist[l_index] is None or l_index is bigger than cpunumbers
        # split linelist[l_index] when there is space in the string
        # then insert the split list into linelist
        if len(linelist) <= l_index or l_index > cpunumbers:
            break
        elif linelist[l_index] \
                and linelist[l_index].find(" ") > -1 \
                and re.match(r"^[\d ]+$|\w+:[\d ]+", linelist[l_index]):
            new_list = linelist[l_index].strip().split()
            teal_list = linelist[l_index+1:]
            linelist = linelist[0:l_index]
            linelist.extend(new_list)
            linelist.extend(teal_list)
            l_index = l_index + len(new_list) - 1
        l_index = l_index + 1

    return linelist


def get_core_num():
        # CPU core num
        proc_cpu_cores = launchcmd('cat /proc/cpuinfo | grep "processor" |wc -l').readline()
        return proc_cpu_cores


def getpercpuinfo():
    stats = []
    # per_info = {}
    flag, node_id = getAgentId()
    # per_info["id"] = node_id
    percpu_times_percent = psutil.cpu_times_percent(interval=0.0, percpu=True)
    for cpu_number, cputimes in enumerate(percpu_times_percent):
        cpu = {'cpu_number': cpu_number,
               'id': node_id,
               'total': round(100 - cputimes.idle, 1),
               'user': cputimes.user,
               'system': cputimes.system,
               'idle': cputimes.idle}
        # The following stats are for API purposes only
        if hasattr(cputimes, 'nice'):
            cpu['nice'] = cputimes.nice
        if hasattr(cputimes, 'iowait'):
            cpu['iowait'] = cputimes.iowait
        if hasattr(cputimes, 'irq'):
            cpu['irq'] = cputimes.irq
        if hasattr(cputimes, 'softirq'):
            cpu['softirq'] = cputimes.softirq
        if hasattr(cputimes, 'steal'):
            cpu['steal'] = cputimes.steal
        if hasattr(cputimes, 'guest'):
            cpu['guest'] = cputimes.guest
        if hasattr(cputimes, 'guest_nice'):
            cpu['guest_nice'] = cputimes.guest_nice
        stats.append(cpu)
    # per_info["body"] = stats
    return stats


def get_total_cpu_info():
    result = {}
    result["cpuload"] = getcpuload()
    result["cpuinfo"] = getcpuinfo()
    result["type"] = "CPU_INFO"
    return result

# Get cpu temperature
def get_cpu_temperature():
    temperature = cpumonitor.deal_cpu_sensor(cpumonitor._plugin_sensors.update())
    return temperature
if __name__ == "__main__":

    print getpercpuinfo()
    # print cpumonitor.deal_cpu_sensor(cpumonitor._plugin_sensors.update())