
"""Process list plugin."""

import os
import commands
import psutil
import ksmp.logger as log


def get_ps_basic_info():
    """

    return:the process list  include basic information
    """
    # pids = get_all_pid()
    result_list = []
    cmd = 'ps -eo pid,vsz,rss,pcpu,pmem,user,time,pri,stat,psr'
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        ps_line = line.split()
        pid = ps_line[0]
        p = int(pid)
        try:
            ps_name = psutil.Process(p).name()
            ps_dict = {
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
        log.error(e)
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
            log.error("ps life cycle error: No such process: "+pid)
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
