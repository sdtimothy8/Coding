"""
this moudule is used to:
 1- create a new service and start with the os
 2- start/stop/restart (a) service(s)
 3- set (a) service(s) start with os or cancel start with os

 last-mod-time: 2016-2-25
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import os

__author__ = 'zhangyuanfang@inspur.com'

onboot_states = {}  # service onboot state dict


class ServiceManage(APIView):

    def get(self, request):
        """
        List all services
        """
        return Response(self.__servicelist(), status=status.HTTP_200_OK)

    def __servicelist(self):
        """
        Get service information
        """
        result = []  # used to return
        self.__onbootstates()

        os.popen('systemctl daemon-reload')

        services = os.popen('systemctl list-units --all --type=service').readlines()
        services = services[1:-7]

        for oneline in services:
            if not oneline.strip():
                continue
            line = oneline.split()
            service = {
                'name': line[0],  # service name
                'load': line[1],  # load
                'active': line[2],  # active
                'sub': line[3],  # sub
                'description': ' '.join(line[4:]),  # service description
                'onboot': self.__getstate(line[0])  # is service start with os
            }
            result.append(service)

        return result

    def __onbootstates(self):
    	"""
        service onboot status dict
        """
        states = os.popen('systemctl list-unit-files --all --type=service').readlines()
        states = states[1:-2]

        for onboot_oneline in states:
            onboot_line = onboot_oneline.split()
            onboot_states[onboot_line[0]] = onboot_line[1]

    def __getstate(self, sname):
    	"""
        get one service onboot state from dict
        """
        if sname in onboot_states:
            return onboot_states[sname]
        return self.__servicestatus(sname)

    def __servicestatus(self, name):
        """
        get each service onboot status
        """
        state = 'unknown'  # initial service status
        output = commands.getoutput('systemctl is-enabled ' + name)
        if ~output.find('is not a native service'):
            newstr = output.split('\n')
            leng = len(newstr)
            state = newstr[leng-1]
        elif output.endswith('No such file or directory'):
            state = 'unknown'
        else:
            state = output

        return state

    def put(self, request):
        """
        start/stop/restart/booton/bootoff
        supply batch operations
        """
        req = request.data
        if ('type' in req) & ('services' in req):  # if 'type' and 'services' in the request
            operation = req['type']
            services = req['services']
            if (operation == '') | (services == ''):  # cannot be null
                return Response('agrs illegal', status=status.HTTP_400_BAD_REQUEST)
            if (operation == 'start') | (operation == 'stop') | (operation == 'restart') | (operation == 'enable') | (operation == 'disable'):
                (ops, result) = self.__opservice(operation, services)
                if ops > 0:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response('operation(s) success', status=status.HTTP_202_ACCEPTED)
            else:
                return Response('agrs illegal', status=status.HTTP_400_BAD_REQUEST)

        else:  # command illegal
            return Response('agrs illegal', status=status.HTTP_400_BAD_REQUEST)

    def __opservice(self, cmd, names):
        """
        execute the service(s) operation, the operation is one of the start/stop/restart/enable/disable
        :param cmd: operation
        :param names: service(s)
        :return:
        """
        count = 0  # set a flag to record operation status
        result = ''  # return string
        for name in names:
            (code, stout) = commands.getstatusoutput('systemctl ' + cmd + ' ' + name['sname'])
            if code != 0:  # command executes failed
                count += 1
                result = result + ' ' + stout
        return count, result
