# coding=utf8
import os
import commands
import psutil
from util import getAgentId
from util import launchcmd


def get_ps_basic_info():
    """

    return:the process list  include basic information
    """
    # pids = get_all_pid()
    result_list = []
    flag, node_id = getAgentId()
    cmd = 'ps -eo pid,vsz,rss,pcpu,pmem,user,time,pri,stat,psr'
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        ps_line = line.split()
        pid = ps_line[0]
        p = int(pid)
        try:
            ps_name = psutil.Process(p).name()
            ps_dict = {
                'nodeId': node_id,
                'pid': pid,
                'name': ps_name,
                'vsz': ps_line[1],
                'rss': ps_line[2],
                'pcpu': ps_line[3],
                'pmem': ps_line[4],
                'user': ps_line[5],
                'time': ps_line[6],
                'pri': ps_line[7],
                'stat': ps_line[8],
                'psr': ps_line[9]
            }
        except psutil.NoSuchProcess:
            continue
        result_list.append(ps_dict)
    return result_list


def get_ps_io(pid):
    """
    get one process io info
    :param pid:
    :return:
    """

    # read_list = commands.getoutput('cat /proc/'+str(p)+'/io |grep "read_bytes"').split(':')
    # write_list = commands.getoutput('cat /proc/'+str(p)+'/io |grep "^write_bytes"').split(':')
    # cancelled_list = commands.getoutput('cat /proc/'+str(p)+'/io |grep "cancelled_write_bytes"').split(':')
    result = []
    try:
        out_list = commands.getoutput('cat /proc/'+pid+'/io').split('\n')
        read = out_list[len(out_list)-3].split(':')[1]
        write = out_list[len(out_list)-2].split(':')[1]
        cancelled = out_list[len(out_list)-1].split(':')[1]
        ret_dict = {
            'pid': pid,
            'read_bytes': read,
            'write_bytes': write,
            'cancelled_write_bytes': cancelled
        }
        result.append(ret_dict)
        return result
    except Exception as e:
        return result


def get_all_pid():
    """

    :return:all system pids
    """
    return psutil.pids()


def get_life_cycle(pid):
    """

    :return:all processes life cycle information
    """
    res_list = command(pid)
    return res_list


def command(pid):
    """

    :return: ps -eo result
    """
    res_list = []
    # cmd = 'ps -eo pid,etime,stime,flag,nice,sched'
    cmd = 'ps -p '+pid+' -o pid,etime,stime,flag,nice,sched'
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        ps_line = line.split()
        p = int(pid)
        try:
            ps_name = psutil.Process(p).name()
            ps_dict = {
                'pid': pid,
                'name': ps_name,
                'etime': ps_line[1],
                'stime': ps_line[2],
                'flag': ps_line[3],
                'nice': ps_line[4],
                'sched': ps_line[5]
            }
        except psutil.NoSuchProcess:
            continue
        res_list.append(ps_dict)
    return res_list


def get_threads(pid):
    """

    :return: threads of the pid
    """
    threads_list = []
    cmd = 'ps -T -p '+pid
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        p_thread = line.split()
        threads_dict = {
            'pid': p_thread[0],
            'spid': p_thread[1],
            'time': p_thread[3],
            'cmd': p_thread[4]
        }
        threads_list.append(threads_dict)
    return threads_list


def get_lsof(pid):
    """

    :param pid:
    :return:the open files information of a system process
    """
    file_list = []
    cmd = 'lsof -p '+pid
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        file_line = line.split()
        if len(file_line) == 9:
            file_dict = {
                'command': file_line[0],
                'pid': file_line[1],
                'user': file_line[2],
                'fd': file_line[3],
                'type': file_line[4],
                'device': file_line[5],
                'size': file_line[6],
                'node': file_line[7],
                'name': file_line[8]
            }
            file_list.append(file_dict)
    return file_list


# 进程预警信息采集
def get_ps_info(itemid):
    psInfo = []
    num = 10
    if "cpu" == itemid:
        commands = "pidstat | sort -k7nr |grep -v 'PID' | head -n " + str(num)
    else:
        commands = "ps -aux|sort -k4nr|grep -v 'USER'|head -n " + str(num)

    try:
        ps_info = launchcmd(commands).readlines()

        for psitem in ps_info:
            if "cpu" == itemid:
                format_iteminfo = format_pidstat_info(psitem)
            else:
                format_iteminfo = format_process_info(psitem)

            if format_iteminfo["pid"].isdigit() and psutil.pid_exists(int(format_iteminfo["pid"])):
                format_iteminfo["name"] = psutil.Process(int(format_iteminfo["pid"])).name()
            else:
                format_iteminfo["name"] = ""
            psInfo.append(format_iteminfo)
    except Exception, e:
        return psInfo
    return psInfo


def format_pidstat_info(item_line):
    """
    Format one process info
    :param item_line:
    :return:
    """
    one_ps = item_line.split()
    pid_dict = {}
    if len(one_ps) < 9:
        pid_dict = {}
    else:
        pid_dict = {
            'time': one_ps[0],
            'uid': one_ps[1],
            'pid': one_ps[2],
            'user': one_ps[3],
            'system': one_ps[4],
            'guest': one_ps[5],
            'cpu': one_ps[6],
            'cpucore': one_ps[7],
            'command': one_ps[8],
        }
    return pid_dict


def format_process_info(ps_line):
    """
    Format one process info
    :param ps_line:
    :return:
    """
    one_ps = ps_line.split()
    if len(one_ps) < 11:
        ps_dict = {}
    else:
        ps_dict = {
            'pid': one_ps[1],
            'user': one_ps[0],
            'cpu': one_ps[2],
            'mem': one_ps[3],
            'vsz': one_ps[4],
            'rss': one_ps[5],
            'start': one_ps[8],
            'command': one_ps[10],
            'tty': one_ps[6],
            'stat': one_ps[7],
            'runtime': one_ps[9]
        }
    return ps_dict


if __name__ == "__main__":
    print get_ps_basic_info()
