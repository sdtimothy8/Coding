"""
TIME for user
"""
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import time
import os
import subprocess


class Synchronoustime(APIView):
    """
    Synchronous time
    ['put']
    """

    def put(self, request, format=None):
        address = request.data
        cmd = "ntpdate -u " + address['addr']
#        cmd = "ntpdate -u " + addr
        (code, resultMSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(resultMSG, status=status.HTTP_200_OK)


class times(APIView):
    """
    set timezone, set system time, set HC time
    ['get', 'put']
    """

    def get(self, request, format=None):
        """
        set timezone
        """

        timezone = {}
        timedate = os.popen('timedatectl').readlines()
        for oneline in timedate:
            if 'Timezone:' in oneline or 'Time zone' in oneline:
                tzStr = oneline[oneline.index(':')+1: oneline.index('(')]
        timezone = {"timezone": tzStr.strip()}
        return Response(timezone, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        """
        set system time or HC time
        """
        timeinfo = request.data
        if(timeinfo['type'] == "localtime"):
            cmd = "timedatectl set-timezone " + timeinfo['time']
            (code, resultMSG) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(resultMSG, status=status.HTTP_200_OK)

        if(timeinfo['type'] == "systohc"):
            (code, result) = commands.getstatusoutput("clock --systohc")
            if code != 0:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return_dict = {"result": "sd", "systohcres": result}

        if(timeinfo['type'] == "hctosys"):
            (code, result) = commands.getstatusoutput("clock --hctosys")
            if code != 0:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return_dict = {"result": "sd", "hctosysres": result}

        cmd = " \""
        if('time' in timeinfo):
            cmd = cmd + timeinfo['time']

        if(timeinfo['type'] == "sysclock"):
            cmd = "date -s" + cmd + "\""
            (code, sysresult) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(sysresult, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return_dict = {"result": sysresult, "systohcres": "dd"}

        if(timeinfo['type'] == "hcclock"):
            cmd = "clock --set --date" + cmd + "\""
            (code, hcresult) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(hcresult, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return_dict = {"result": hcresult, "hctosysres": "dd"}
        return Response(return_dict, status=status.HTTP_200_OK)


class ssltime(APIView):
    '''
    get apache ssl time range
    '''

    def get(self, request, format=None):
        matchstr = "%a %b %d %H:%M:%S %Y"
        lines = os.popen('certutil -d /etc/httpd/alias -L -n Server-Cert')
        strline = ''
        endline = ''
        for line in lines:
            if 'Not Before' in line:
                strline = line
            if 'Not After' in line:
                endline = line
                break
        if strline == '' or endline == '':
            return Response('no specified', status=status.HTTP_200_OK)

        strline = strline.strip()
        endline = endline.strip()
        start = strline.split(': ')
        end = endline.split(': ')
        try:
            strtime = start[1].strip()
            endtime = end[1].strip()
        except IndexError:
            return Response('not find', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            start_float_time = time.mktime(time.strptime(strtime, matchstr))
            end_float_time = time.mktime(time.strptime(endtime, matchstr))
            return Response(data={'start': start_float_time, 'end': end_float_time}, status=status.HTTP_200_OK)


class currentTime(APIView):
    '''
    get current system time
    '''
    def get(self, request, format=None):
        timestr = []
        cmds = ['clock -r', 'date -R']
        for i in range(len(cmds)):
            proc = subprocess.Popen(cmds[i], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdoutput, stderrput) = proc.communicate()
            if proc.returncode == 0:
                timestr.append(stdoutput)
            else:
                continue
        if len(timestr) != len(cmds):
            return Response(data='error1', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        currenttime = timestr[-1].split(' ')
        if len(currenttime) >= 6:
            tz = currenttime[-1].strip()
        else:
            return Response(data='error2', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        hwresult = timestr[0].split('  ')
        if len(hwresult) == 2:
            hwtimestr = hwresult[0]
        elif len(hwresult) == 3:
            hwtimestr = hwresult[0] + ' ' + hwresult[1]
        else:
            return Response(data='error3', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        hwtime = time.mktime(time.strptime(hwtimestr, '%a %b %d %H:%M:%S %Y'))  # - float(hwresult[2].split(' ')[0])
        systime = time.time()
        return Response(data={'timezone': int(tz)/100, 'hardwaretime': hwtime, 'systemtime': systime}, status=status.HTTP_200_OK)
