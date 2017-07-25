"""
The main module for get add and delete precmd.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import commands
from public import functions

__author__ = 'xiek@inspur.com'


class CmdList(APIView):
    """
    List all precmd
    """
    def get(self, request, format=None):
        """
        Get precmd list.
        """
        cmdlines = os.popen('atq').readlines()
        cmd = []
        for oneline in cmdlines:
            cmdtemp = oneline.split()
            cmddict = {
                'num': cmdtemp[0],
                'user': cmdtemp[7],
                'time': cmdtemp[1] + ' ' + cmdtemp[2] + ' ' + cmdtemp[3] + ' ' + cmdtemp[4] + ' ' + cmdtemp[5]
            }
            cmd.append(cmddict)
        return Response(cmd, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        craet one schedual cmd.
        """
        req = request.data
        username = req['username']
        time = req['time']
        path = req['path']
        cmd = req['cmd']

        at_file = open('/tmp/at.txt', 'w')
        try:
            at_file.write(cmd)
        finally:
            at_file.close()
        command = "cd " + path + " && su " + username + " -c 'at " + time + " -f " + "/tmp/at.txt'"
        code, info = commands.getstatusoutput(command)
        # print(info)
        if os.path.exists('/tmp/at.txt'):
            os.remove('/tmp/at.txt')
        if (code != 0):
            return Response(info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(info, status=status.HTTP_201_CREATED)


class CmdDetail(APIView):
    """
    Provide the method for processing schedulcmd.
    Add, get, delete one item.
    """
    def get(self, request, cmdnum, format=None):
        """
        Get detail of one precmd.
        """
        shell_line = os.popen('at -c ' + cmdnum).readlines()
        cmdstr = {"cmdinfo": shell_line}
        return Response(cmdstr, status=status.HTTP_200_OK)

    def delete(self, request, cmdnum, format=None):
        """
        Delete one precmd.
        """
        errdict = {"errinfo": []}
        numarr = cmdnum.split(',')
        for onenum in numarr:
            code, info = commands.getstatusoutput('atrm ' + onenum)
            if (code != 0):
                errdict["errcode"] = code
                errdict["errinfo"].append({onenum: info})
            else:
                errdict["errinfo"].append({onenum: "delete success"})
        if "errcode" in errdict:
            return Response(errdict, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(errdict, status=status.HTTP_200_OK)
