"""
 This module for system monitoring related features
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.servicecpu import cpumonitor
from service.servicefs import fsmonitor
from service.servicedisk import diskmonitor
from sysmonitor.plugins.unicorn_mem_business import MemBusiness
from sysmonitor.plugins.unicorn_network_io import NetworkIO
from ksmp import util, message
from ksmp import logger
from ksmp import message
from plugins import unicon_processlist as processlist
import psutil
from sysmonitor.models import MemBasicInfo as mem_history
from sysmonitor.models import CpuLoadBasicInfo as cpu_history
from sysmonitor.models import DiskioBasicInfo as disk_history
__author__ = 'caofengbing@inspur.com'

# Create your views here.


class CpuList(APIView):
    """
    get info for cpu load,base,interrupts...
    """
    def get(self, request, itemid, format=None):
        """
        get method of cpu monitor
        """
        retflg, retstr = cpumonitor.update_stats(request, itemid)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileSystemList(APIView):
    """
    get info of file system
    """
    def get(self, request, itemid, format=None):
        """
        get method of file system monitor
        """
        retflg, retstr = fsmonitor.update_stats(request, itemid)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DiskList(APIView):
    """
    get info of disk io\ block
    """
    def get(self, request, itemid, format=None):
        """
        get method of disk monitor
        """
        retflg, retstr = diskmonitor.update_stats(request, itemid)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProcessList(APIView):

    """
     List all process  basic infomation
    """
    def get(self, request, format=None):
        """
        Get process list.
        """
        all_process = processlist.get_ps_basic_info()
        return Response(all_process, status=status.HTTP_200_OK)


class ProcessLifeCycleList(APIView):
    """
    List all process life cycle information

    """
    def get(self,request, format=None):
        """
        Get one process life cycle

        """
        pid = request.GET.get('pid')
        if not pid.isdigit():
            return Response('the pid is invalid')
        if psutil.pid_exists(int(pid)):
            life_cycle_info = processlist.get_life_cycle(pid)
            return Response(life_cycle_info, status=status.HTTP_200_OK)
        else:
            return Response('the pid is not exist', status=status.HTTP_400_BAD_REQUEST)


class ProcessIOList(APIView):
    """
    List all process IO information

    """
    def get(self,request, format=None):
        """

        Get one process io info
        """
        pid = request.GET.get('pid')
        if not pid.isdigit():
            return Response('the pid is invalid')
        if psutil.pid_exists(int(pid)):
            ps_io = processlist.get_ps_io(pid)
            return Response(ps_io, status=status.HTTP_200_OK)
        else:
            return Response('the pid is not exist', status=status.HTTP_400_BAD_REQUEST)


class ProcessThreadsList(APIView):
    """
    List a process threads information
    """
    def get(self, request, format=None):
        """

        Get process threads
        """
        pid = request.GET.get('pid')
        if not pid.isdigit():
            return Response('the pid is invalid')
        if psutil.pid_exists(int(pid)):
            threads_list = processlist.get_threads(pid)
            return Response(threads_list, status=status.HTTP_200_OK)
        else:
            return Response('the pid is not exist', status=status.HTTP_400_BAD_REQUEST)


class ProcessFileList(APIView):
    """
    List a process threads information
    """
    def get(self, request, format=None):
        """

        Get open files of a process
        """
        pid = request.GET.get('pid')
        if not pid.isdigit():
            return Response('the pid is invalid')
        if psutil.pid_exists(int(pid)):
            file_list = processlist.get_lsof(str(pid))
            return Response(file_list, status=status.HTTP_200_OK)
        else:
            return Response('the pid is not exist', status=status.HTTP_400_BAD_REQUEST)


class MemBasicInfo(APIView):
    """
    show basic basic info
    """

    def get(self, request, format=None):

        keys = ["all"]
        if request.GET.get("keys"):
            keys = request.GET["keys"].replace("[", "").replace("]", "").replace("\"", "").split(",")
        logger.debug(keys)

        rtn_flag, rtn_basic_info = MemBusiness.get_mem_info(keys)

        if rtn_flag:
            return Response({"meminfo": rtn_basic_info}, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MemSwapInfo(APIView):
    """
    show memory basic info
    """

    def get(self, request, format=None):

        keys = ["all"]
        if request.GET.get("keys"):
            keys = request.GET["keys"].replace("[", "").replace("]", "").replace("\"", "").split(",")
        logger.debug(keys)

        rtn_flag, rtn_swap_info = MemBusiness.get_swap_info(keys)

        if rtn_flag:
            return Response({"swapinfo": rtn_swap_info}, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PageInfo(APIView):
    """
    show memory page info
    """

    def get(self, request, format=None):

        keys = ["all"]
        if request.GET.get("keys"):
            keys = request.GET["keys"].replace("[", "").replace("]", "").replace("\"", "").split(",")
        logger.debug(keys)

        rtn_flag, rtn_page_info = MemBusiness.get_page_info(keys)

        if rtn_flag:
            return Response({"pageinfo": rtn_page_info}, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SlabInfo(APIView):
    """
    show slab info
    """

    def get(self, request, format=None):

        keys = ["all"]
        name = ""
        if request.GET.get("keys"):
            keys = request.GET["keys"].replace("[", "").replace("]", "").replace("\"", "").split(",")

        if request.GET.get("name"):
            name = request.GET["name"]
        logger.debug(keys)
        logger.debug(name)

        rtn_flag, rtn_slab_info = MemBusiness.get_slab_info(name, keys)

        if rtn_flag:
            return Response({"slabinfo": rtn_slab_info}, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NumastatInfo(APIView):
    """
    show numastat info
    """

    def get(self, request, format=None):

        rtn_flag, rtn_numastat_info = MemBusiness.get_numastat_info()

        if rtn_flag:
            return Response({"numastat": rtn_numastat_info}, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThroughputInfo(APIView):
    """
    show through put info
    """

    def get(self, request, format=None):

        rtn_flag, rtn_throughput_info = NetworkIO.get_throughput_info()

        if rtn_flag:
            return Response(rtn_throughput_info, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocketInfo(APIView):
    """
    show socket info
    """

    def get(self, request, format=None):

        rtn_flag, rtn_socket_info = NetworkIO.get_socket_info()

        if rtn_flag:
            return Response(rtn_socket_info, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IptraficInfo(APIView):
    """
    show ip trafic info
    """

    def get(self, request, format=None):

        rtn_flag, rtn_iptrafic_info = NetworkIO.get_iptrafic_info()

        if rtn_flag:
            return Response(rtn_iptrafic_info, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TCPInfo(APIView):
    """
    show tcp info
    """

    def get(self, request, format=None):
        rtn_flag, rtn_tcp_info = NetworkIO.get_tcp_info()

        if rtn_flag:
            return Response(rtn_tcp_info, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UDPInfo(APIView):
    """
    show udp info
    """

    def get(self, request, format=None):

        rtn_flag, rtn_udp_info = NetworkIO.get_udp_info()

        if rtn_flag:
            return Response(rtn_udp_info, status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MemHistoryInfo(APIView):
    """
    read history info from db
    """

    def get(self, request, format=None):

        percent = []
        rtn_info = mem_history.objects.order_by("id")

        for info in rtn_info:
            percent.append(info.percent)
        logger.debug(percent)

        return Response({"mem_percent": percent}, status=status.HTTP_200_OK)


class CpuHistoryInfo(APIView):
    """
    read history info from db
    """

    def get(self, request, format=None):

        load_infos = []
        rtn_info = cpu_history.objects.order_by("id")

        for info in rtn_info:
            dick_info = {"min1": info.oneminute,
                         "min5": info.fiveminute,
                         "min15": info.fifteenminute}
            load_infos.append(dick_info)
        logger.debug(load_infos)

        return Response(load_infos, status=status.HTTP_200_OK)


class DiskHistoryInfo(APIView):
    """
    read history info from db
    """

    def get(self, request, format=None):

        tps_list = []
        rtn_info = disk_history.objects.order_by("id")

        for info in rtn_info:
            tps_list.append({"tpsnum": info.tpsnum})
        logger.debug(tps_list)

        return Response(tps_list, status=status.HTTP_200_OK)
