# __author__ = 'root'
import subprocess
import os
import pika
import json
from string import strip
import time
import sys
import traceback
import psutil
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
    node_id = 1
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

# if __name__ == "__main__":
#    flag, ip = getRabbitmqIp()
#    print ip
