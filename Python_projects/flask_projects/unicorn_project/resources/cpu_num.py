# coding:utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
from public import functions


reload(sys)
sys.setdefaultencoding('utf8')

class CpuNumView(APIView):
    """
    For resources sysInfo
    """

    def get(self, request, format=None):
        """
        GET  sysInfo
        """

        sysinfo = {}

        # CPU core num
        proc_cpu_cores = functions.launchcmd('cat /proc/cpuinfo | grep "processor" |wc -l').readline()
        # logging.debug("cpu_num = " + cpu_num)

        sysinfo["cpunum"] = int(proc_cpu_cores.strip())

        # install soft

        return Response(sysinfo, status=status.HTTP_200_OK)
