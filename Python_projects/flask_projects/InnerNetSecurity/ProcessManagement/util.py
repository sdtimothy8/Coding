# __author__ = 'root'
import subprocess
import os
import pika
import json
from string import strip
import time
import sys
# import logging
# from ksmp import settings
# from ksmp import logger
# from agent.utils import getServerInfo

def getAllProcesses():
    """
    return:the process list  include basic information
    """
    result_list = []
    #Todo: flag, node_id = getAgentId()
    cmd = 'ps -eo pid,vsz,rss,pcpu,pmem,user,time,pri,stat,psr,comm'
    res = os.popen(cmd).readlines()
    for line in res[1:len(res)]:
        ps_line = line.split()
        ps_dict = {
            'pid': int(ps_line[0]),
            'vsz': ps_line[1],
            'rss': ps_line[2],
            'pcpu': ps_line[3],
            'pmem': ps_line[4],
            'user': ps_line[5],
            'time': ps_line[6],
            'pri': ps_line[7],
            'stat': ps_line[8],
            'psr': ps_line[9],
            'name': ps_line[10]
        }
        result_list.append(ps_dict)

    return result_list

def getConditionalProcesses( userName, processPid, program):
    """
    return:the process list  include basic information
    """
    result_list = []
    #Todo: flag, node_id = getAgentId()
    cmd = 'ps -eo pid,vsz,rss,pcpu,pmem,user,time,pri,stat,psr,comm'
    if len(processPid) != 0:
        cmd = cmd + " |awk '$1 == %s{print $0}'" %processPid
    else:
        if len(userName) != 0:
            cmd = cmd + " |awk '$6 == \"%s\"{print $0}'" %userName

        if len(program) != 0:
            cmd = cmd + " | grep %s" %program

    print cmd
    res = os.popen(cmd).readlines()
    for line in res:
        ps_line = line.split()
        ps_dict = {
            'pid': int(ps_line[0]),
            'vsz': ps_line[1],
            'rss': ps_line[2],
            'pcpu': ps_line[3],
            'pmem': ps_line[4],
            'user': ps_line[5],
            'time': ps_line[6],
            'pri': ps_line[7],
            'stat': ps_line[8],
            'psr': ps_line[9],
            'name': ps_line[10]
        }
        result_list.append(ps_dict)

    return result_list


# if __name__ == "__main__":
#    flag, ip = getRabbitmqIp()
#    print ip
