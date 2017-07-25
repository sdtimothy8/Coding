# coding:utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import subprocess
import sys
import psutil
from public import functions
from ksmp import logger
from resources.models import NetIOInfo as net_histroy

# import logging
# logging.basicConfig(filename='/var/log/ksmp/resources.log', level=logging.DEBUG)

__author__ = 'zhuysh@inspur.com'

# Create your views here.

reload(sys)
sys.setdefaultencoding('utf8')

try:
    import simplejson as json
except Exception, e:
    import json


class ResourceList(APIView):
    """
    For resources sysInfo
    """

    def get(self, request, format=None):
        """
        GET  sysInfo
        """

        sysinfo = {}

        # kenal version
        # version = commands.getoutput('uname -r')
        # version = self.commoncmd('uname -r')
        version = functions.launchcmd('uname -r').readline().strip('\n')
        sysinfo["version"] = version

        # CPU info
        # cpuInfo = commands.getoutput('cat /proc/cpuinfo |grep "name" |cut -f2 -d: |uniq')
        # cpuinfo = self.commoncmd('cat /proc/cpuinfo |grep "name" |cut -f2 -d: |uniq')
        cpuinfo = functions.launchcmd('cat /proc/cpuinfo |grep "name" |cut -f2 -d: |uniq').readline().strip('\n')
        sysinfo["cpuInfo"] = cpuinfo

        # CPU load average
        # upTimeInfo = commands.getoutput('uptime')
        # uptimeinfo = self.commoncmd('uptime')
        uptimeinfo = functions.launchcmd('uptime').readline().strip('\n')
        loadaverage = uptimeinfo.split('average:')[1]
        sysinfo["loadAverage"] = loadaverage

        # memory info
        # freem = os.popen('free -m').readlines()
        freem = functions.launchcmd('free -m').readlines()
        for tempmen in freem[1:len(freem)]:
            men = tempmen.split()
            meninfo = {
                'name': men[0],
                'total': men[1],
                'used': men[2],
                'free': men[3]
            }
            sysinfo[men[0].split(':')[0]] = meninfo

        # hostname
        # hostname = self.commoncmd('uname -n')
        hostname = functions.launchcmd('uname -n').readline().strip('\n')
        sysinfo["hostname"] = hostname

        # sysversion
        if(os.path.exists("/etc/redhat-release")):
            sysversion = functions.launchcmd('cat /etc/redhat-release').readline().strip('\n')
        elif(os.path.exists("/etc/inspur-release")):
            sysversion = functions.launchcmd('cat /etc/inspur-release').readline().strip('\n')

        sysinfo["systemversion"] = sysversion

        # starttime
        # starttime = self.commoncmd('uptime -s')
        starttime = functions.launchcmd('uptime -s').readline().strip('\n')
        sysinfo["starttime"] = starttime

        # runtime
        # runtimestr = self.commoncmd('uptime -p')
        runtimestr = functions.launchcmd('uptime -p').readline().strip('\n')
        runtime = runtimestr[3:]
        sysinfo["runningtime"] = runtime

        # currenttime
        # currenttime = self.commoncmd('date +%Y-%m-%d\' \'%k:%M:%S')
        currenttime = functions.launchcmd('date +%Y-%m-%d\' \'%k:%M:%S').readline().strip('\n')
        sysinfo["currenttime"] = currenttime

        # disk info
        # disklines=os.popen('df -Th').readlines()
        disklines = functions.launchcmd('df -Th').readlines()
        diskinfo = []
        for diskline in disklines[1:len(disklines)]:
            onedisk = diskline.split()
            print onedisk
            oneDisk = {
                'Filesystem': onedisk[0],
                'Type': onedisk[1],
                'Size': onedisk[2],
                'Used': onedisk[3],
                'Avail': onedisk[4],
                'Usepersent': onedisk[5],
                'Mounted on': onedisk[6]
            }
            diskinfo.append(oneDisk)

        sysinfo["diskinfo"] = diskinfo

        # CPU core num
        cpu_num = functions.launchcmd('cat /proc/cpuinfo |grep "physical id" |sort | uniq|wc -l').readline()
        each_cpu_cores = functions.launchcmd('cat /proc/cpuinfo | grep "cpu cores"|cut -d: -f2|uniq').readline()
        proc_cpu_cores = functions.launchcmd('cat /proc/cpuinfo | grep "processor" |wc -l').readline()
        # logging.debug("cpu_num = " + cpu_num)
        # logging.debug("each_cpu_cores = " + each_cpu_cores)
        # logging.debug("proc_cpu_cores = " + proc_cpu_cores)

        phy_cpu_cores = int(cpu_num) * int(each_cpu_cores)
        sysinfo["phycpucores"] = phy_cpu_cores
        sysinfo["proc_cpu_cores"] = proc_cpu_cores
        sysinfo["cpu_num"] = cpu_num

        # install soft
        installsoftnum = functions.launchcmd('rpm -qa|wc -l').readline()
        sysinfo["installsoftnum"] = installsoftnum

        # login users
        users = functions.launchcmd("who | cut -d' ' -f1 |sort | uniq").readlines()
        usersinfo = ""
        for user in users:
            usersinfo = usersinfo + user + " "
        sysinfo["users"] = usersinfo

        return Response(sysinfo, status=status.HTTP_200_OK)

    # def commoncmd(self, cmd):
    #     (status, output) = commands.getstatusoutput(cmd)
    #     print status
    #     if status == 0:
    #         return output
    #     else:
    #         return "falied to get information"


class ResourcePciList(APIView):
    """
    List all pci  items, or create a new one.
    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """

    def get(self, request, format=None):
        """
        Get pci list.
        """
        # Add your code here.

        pci_devices = functions.launchcmd('lspci').readlines()
        pci_info = []
        for pci_device in pci_devices:
            pci_info.append(pci_device)
        return Response(pci_info, status=status.HTTP_200_OK)


class ResourceUsbList(APIView):
    """
    List all ResourcesUsbList items, or create a new one.
    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """

    def get(self, request, format=None):
        """
        Get usb list.
        """
        # Add your code here.
        # usbdevices=os.popen('lsusb').readlines()
        usb_devices = functions.launchcmd('lsusb').readlines()
        usb_info = []
        for usb_device in usb_devices:
            usb_info.append(usb_device)
        return Response(usb_info, status=status.HTTP_200_OK)


class PsList(APIView):
    """
    List all firewall items, or create a new one.
    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """
    def get(self, request, format=None):
        """
        Get ps list.
        """
        ps_lines = os.popen('ps -aux').readlines()
        ps_info = []
        for ps_line in ps_lines[1: len(ps_lines)]:
            ps_info.append(format_process_info(ps_line))
        return Response(ps_info, status=status.HTTP_200_OK)


class PsDetail(APIView):
    """
    Provide the methods for processing one ps item.
    Get ,delete one item.
    """
    def get(self, request, format=None):

        # Get ps detail item.

        usr = request.GET.get('user', '')
        pid = request.GET.get('pid', '')
        ps_name = request.GET.get('psname', '')
        ps_info = []
        if pid != '':
            ps_info = get_process_from_pid(pid)
        else:
            ps_info = get_process_from_match_info(usr, ps_name)
        if len(ps_info) > 0:
            return Response(ps_info, status=status.HTTP_200_OK)
        else:
            return Response('No Such Processes', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        1,Delete selected ps item.
        """
        result = 0
        pid = request.data.get('pid', None)
        if pid is not None:
            cmd = 'kill -9 '+pid
            result = os.system(cmd)
        else:
            return Response('delete fail,the pid is none!', status=status.HTTP_400_BAD_REQUEST)
        if result == 0:
            return Response("delete success", status=status.HTTP_200_OK)
        else:
            return Response('delete fail', status=status.HTTP_400_BAD_REQUEST)


def format_process_info(ps_line):
    """
    Format one process info
    :param ps_line:
    :return:
    """
    one_ps = ps_line.split()
    ps_dict = {}
    if len(one_ps) < 11:
        ps_dict = {
            'pid': "",
            'user': "",
            'cpu': "",
            'mem': "",
            'vsz': "",
            'rss': "",
            'start': "",
            'command': "",
            'tty': "",
            'stat': "",
            'runtime': ""
        }
    else:
        ps_dict = {
            'pid': one_ps[1],
            'user': one_ps[0],
            'cpu': one_ps[2],
            'mem': one_ps[3],
            'vsz': one_ps[4],
            'rss': one_ps[5],
            'start': one_ps[8],
            'command': one_ps[10],
            'tty': one_ps[6],
            'stat': one_ps[7],
            'runtime': one_ps[9]
        }
    return ps_dict


def get_process_from_pid(pid):
    """
    get a process from proces ID
    :param pid:
    :return:
    """
    find_info = 'ps -aux'
    ps_detail_list = subprocess.Popen(find_info, stdout=subprocess.PIPE, shell=True).stdout.readlines()
    ps_info = []
    for ps_line in ps_detail_list[1:len(ps_detail_list)]:
        one_ps = ps_line.split()
        if pid == one_ps[1]:
            ps_info.append(format_process_info(ps_line))
            break
    return ps_info


def get_process_from_match_info(user, psname):
    """
    get all processes  from user and process info
    :param user:
    :param psname:
    :return:
    """
    find_info = 'ps -aux'
    ps_detail_list = subprocess.Popen(find_info, stdout=subprocess.PIPE, shell=True).stdout.readlines()
    ps_info = []
    if user != '' and psname != '':
        for ps_line in ps_detail_list[1:len(ps_detail_list)]:
            one_ps = ps_line.split()
            if one_ps[0].find(user) != -1 and one_ps[10].find(psname) != -1:
                ps_info.append(format_process_info(ps_line))
    elif user != '':
        for ps_line in ps_detail_list[1:len(ps_detail_list)]:
            one_ps = ps_line.split()
            if one_ps[0].find(user) != -1:
                ps_info.append(format_process_info(ps_line))
    elif psname != '':
        for ps_line in ps_detail_list[1:len(ps_detail_list)]:
            one_ps = ps_line.split()
            if one_ps[10].find(psname) != -1:
                ps_info.append(format_process_info(ps_line))
    else:
        return ps_info
    return ps_info


class PsCpuMemInfo(APIView):
    """
    the process of CPU and memory info
    """

    def get(self, request, format=None):
        psMemCpuInfo = {}

        commands_MEM = "ps -aux|sort -k4nr|grep -v 'USER'|head -n 1"
        commands_CPU = "ps -aux|sort -k3nr|grep -v 'USER'|head -n 1"

        try:
            ps_MEM_info = functions.launchcmd(commands_MEM).readline()
            ps_CPU_info = functions.launchcmd(commands_CPU).readline()
            logger.debug("ps_MEM_info ===> " + ps_MEM_info)
            logger.debug("ps_CPU_info ===> " + ps_CPU_info)

            psMemCpuInfo["psmeminfo"] = format_process_info(ps_MEM_info)
            if psMemCpuInfo["psmeminfo"]["pid"].isdigit() and psutil.pid_exists(int(psMemCpuInfo["psmeminfo"]["pid"])):
                psMemCpuInfo["psmeminfo"]["name"] = psutil.Process(int(psMemCpuInfo["psmeminfo"]["pid"])).name()
            else:
                psMemCpuInfo["psmeminfo"]["name"] = ""
            psMemCpuInfo["pscpuinfo"] = format_process_info(ps_CPU_info)
            if psMemCpuInfo["pscpuinfo"]["pid"].isdigit() and psutil.pid_exists(int(psMemCpuInfo["pscpuinfo"]["pid"])):
                psMemCpuInfo["pscpuinfo"]["name"] = psutil.Process(int(psMemCpuInfo["pscpuinfo"]["pid"])).name()
            else:
                psMemCpuInfo["pscpuinfo"]["name"] = ""
        except Exception, exception:
            logger.error("PsCpuMemInfo error! ===> " + exception.message)
            return Response(psMemCpuInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(psMemCpuInfo, status=status.HTTP_200_OK)


class NetIOInfo(APIView):
    """
    the network IO info
    """

    def get(self, request, format=None):

        logger.debug("net begin:")
        netinfo = {}

        try:
            commands_net = "sar -n DEV 1 1"
            logger.debug(commands_net)
            net_info_list = subprocess.Popen(commands_net, stdout=subprocess.PIPE, shell=True).stdout.readlines()

            logger.debug("commands finshed!")

            rx = 0
            tx = 0

            for net_info in net_info_list:
                if -1 != net_info.find("：") or -1 != net_info.find(":"):
                    if -1 == net_info.find("rxkB"):
                        rx = rx + float(net_info.split()[4])
                        tx = tx + float(net_info.split()[5])

            netinfo["rx"] = rx
            netinfo["tx"] = tx
        except Exception, exception:
            logger.error("NetIOInfo error ===> " + exception.message)
            return Response(netinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(netinfo, status=status.HTTP_200_OK)


class DiskIOInfo(APIView):
    """
    the process holding most of disk IO resource
    """

    def get(self, request, format=None):

        disk_ps_info = {}

        try:
            logger.debug("diskinfo begin--------------")
            net_info_list = functions.launchcmd('iotop -P -b -n 1 | head -n 4').readlines()
            logger.debug("net_info_list -1 ====== " + net_info_list[-1])
            disk_ps_info["psdiskinfo"] = net_info_list[-1].split()[0]
            logger.debug("psdiskinfo ===> " + disk_ps_info["psdiskinfo"])
            if disk_ps_info["psdiskinfo"].isdigit() and psutil.pid_exists(int(disk_ps_info["psdiskinfo"])):
                disk_ps_info["name"] = psutil.Process(int(disk_ps_info["psdiskinfo"])).name()
            else:
                disk_ps_info["name"] = ""
        except Exception, exception:
            logger.error("DiskIOInfo error!===>" + exception.message)
            return Response(disk_ps_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(disk_ps_info, status=status.HTTP_200_OK)


class NetHistoryInfo(APIView):
    """
    read history info from db
    """

    def get(self, request, format=None):

        total_history = []
        rtn_info = net_histroy.objects.order_by("id")

        for info in rtn_info:
            total_history.append(info.total)
        logger.debug(total_history)

        return Response({"net_total": total_history}, status=status.HTTP_200_OK)


class PsListInfo(APIView):
    """
    List all process items.
    """
    def get(self, request, itemid, format=None):
        """
        Get ps list.
        """
        psInfo = []
        commands = ""
        num = 10
        if request.GET.get("num"):
            num = request.GET["num"]

        if "cpu" == itemid:
            commands = "pidstat | sort -k7nr |grep -v 'PID' | head -n " + str(num)
        else:
            commands = "ps -aux|sort -k4nr|grep -v 'USER'|head -n " + str(num)

        try:
            ps_info = functions.launchcmd(commands).readlines()

            for psitem in ps_info:
                format_iteminfo = []
                if "cpu" == itemid:
                    format_iteminfo = format_pidstat_info(psitem)
                else:
                    format_iteminfo = format_process_info(psitem)

                if format_iteminfo["pid"].isdigit() and psutil.pid_exists(int(format_iteminfo["pid"])):
                    format_iteminfo["name"] = psutil.Process(int(format_iteminfo["pid"])).name()
                else:
                    format_iteminfo["name"] = ""
                psInfo.append(format_iteminfo)
        except Exception, exception:
            logger.error("PsInfo error! ===> " + exception.message)

        return Response(psInfo, status=status.HTTP_200_OK)


def format_pidstat_info(item_line):
    """
    Format one process info
    :param item_line:
    :return:
    """
    one_ps = item_line.split()
    pid_dict = {}
    if len(one_ps) < 9:
        pid_dict = {
            'time': "",
            'uid': "",
            'pid': "",
            'user': "",
            'system': "",
            'guest': "",
            'cpu': "",
            'cpucore': "",
            'command': "",
        }
    else:
        pid_dict = {
            'time': one_ps[0],
            'uid': one_ps[1],
            'pid': one_ps[2],
            'user': one_ps[3],
            'system': one_ps[4],
            'guest': one_ps[5],
            'cpu': one_ps[6],
            'cpucore': one_ps[7],
            'command': one_ps[8],
        }
    return pid_dict
