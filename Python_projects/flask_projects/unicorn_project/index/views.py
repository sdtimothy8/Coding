# coding=utf8
'''
this module is used to provide basic i
'''
import subprocess
import re
import time
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Index(APIView):
    '''
    for system basic information request.
    '''

    def get(self, Request, format=None):
        pattern = re.compile(r'^[^\\]*')
        CMDs = ['hostname',
                'cat /etc/inspur-release',
                'uname -r',
                # 'cat /proc/version',
                'date -R']
        outputKey = ['HostName', 'System version', 'System kernel', 'Date']

        CPUCMD = 'cat /proc/cpuinfo | grep \'model name\' | head -1'

        SysRunningTime = 'cat /proc/uptime| awk -F. \'{run_days=$1 / 86400;\
            run_hour=($1 % 86400)/3600;\
            run_minute=($1 % 3600)/60;run_second=$1 % 60;\
            printf("%d 天, %d 时, %d 分, %d 秒",run_days,\
            run_hour,run_minute,run_second)}\''

        indexJsonOutput = []
        if len(CMDs) != len(outputKey):
            return Response(
                    "internal server error",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        for item in range(len(CMDs)):
            proc = subprocess.Popen(
                        CMDs[item],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE)
            (stdoutput, erroroutput) = proc.communicate()
            match = pattern.match(stdoutput)
            if match:
                output = match.group()
            if proc.returncode == 0:
                indexJsonOutput.append(
                    {"key": outputKey[item], "value": output.strip()})
            else:
                continue
        proc = subprocess.Popen(
                    CPUCMD,
                    shell=True,
                    close_fds=True,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        (stdoutput, errorput) = proc.communicate()
        if proc.returncode == 0:
            indexJsonOutput.append(
                {'key': 'CPU', 'value': stdoutput.strip().split(":")[1]})
        proc = subprocess.Popen(
                    SysRunningTime,
                    shell=True,
                    close_fds=True,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        (stdoutput, errorput) = proc.communicate()

        if proc.returncode == 0:
            indexJsonOutput.append(
                {'key': 'System running time', 'value': stdoutput.strip()})
        return Response(indexJsonOutput, status=status.HTTP_200_OK)


class Systime(APIView):
    '''
    get system time
    '''

    def get(request, response, format=None):
        data = time.time()
        return Response(data, status=status.HTTP_200_OK)
