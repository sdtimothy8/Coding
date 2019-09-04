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

def getServiceList():
    """
    Get service information
    """
    result_list = []  # used to return

    os.popen('systemctl daemon-reload')

    services = os.popen('systemctl list-units --all --type=service').readlines()
    services = services[1:-7]

    for oneline in services:
        if not oneline.strip():
            continue
        line = oneline.split()
        service = {
            'seriveName': line[0],  # service name
            'loadStatus': line[1],  # load
            'status': line[2],  # active
            'sub': line[3],  # sub
            'description': ' '.join(line[4:]),  # service description
        }
        result_list.append(service)

    return result_list


def getConditionalServiceList(serviceName, status):
    """
    Get service information based on search condition
    """
    result_list = []  # used to return
    os.popen('systemctl daemon-reload')
    cmd = 'systemctl list-units --all --type=service'
    
    if len(serviceName) != 0:
        cmd = cmd + ' |grep %s' %serviceName
    
    if len(status) != 0:
        cmd = cmd + ' |grep %s' %status
    print cmd
    services = os.popen(cmd).readlines()
    print services

    for oneline in services:
        if not oneline.strip():
            continue
        line = oneline.split()
        service = {
            'seriveName': line[0],  # service name
            'loadStatus': line[1],  # load
            'status': line[2],  # active
            'sub': line[3],  # sub
            'description': ' '.join(line[4:]),  # service description
        }
        result_list.append(service)

    return result_list




# if __name__ == "__main__":
#    flag, ip = getRabbitmqIp()
#    print ip
