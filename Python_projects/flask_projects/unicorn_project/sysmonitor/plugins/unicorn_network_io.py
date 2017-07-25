"""
This module provide classes for monitor Memory info
"""
from public import functions
from ksmp import logger


__author__ = 'zhangguolei@inspur.com'


class NetworkIO():
    """
    this class provides methods for memory monitor
    """

    @classmethod
    def get_throughput_info(cls):
        """
        get throughput info
        :return:
        """

        throughput_list = {}

        try:
            logger.debug("throughput begin:======>")
            rtinfo = functions.launchcmd('sar -n ALL 1 1').readlines()
            logger.debug("commands finished! ")
            if rtinfo:
                continue_falg = True
                falg = True
                for item in rtinfo:
                    throughput_info = {}
                    if continue_falg:
                        if "IFACE" in item:
                            continue_falg = False
                        continue
                    if "rxerr" in item:
                        falg = False
                        continue
                    if "call" in item:
                        break
                    tmplist = item.split()
                    if tmplist is None or tmplist == []:
                        continue
                    if falg:
                        throughput_info["time"] = tmplist[0]
                        throughput_info["name"] = tmplist[1]
                        throughput_info["rxpck/s"] = tmplist[2]
                        throughput_info["txpck/s"] = tmplist[3]
                        throughput_info["rxkB/s"] = tmplist[4]
                        throughput_info["txkB/s"] = tmplist[5]
                        throughput_info["rxcmp/s"] = tmplist[6]
                        throughput_info["txcmp/s"] = tmplist[7]
                        throughput_info["rxmcst/s"] = tmplist[8]

                        throughput_list[tmplist[1]] = throughput_info
                    else:
                        throughput_info = throughput_list[tmplist[1]]
                        throughput_info["rxerr/s"] = tmplist[2]
                        throughput_info["txerr/s"] = tmplist[3]
                        throughput_info["coll/s"] = tmplist[4]
                        throughput_info["rxdrop/s"] = tmplist[5]
                        throughput_info["txdrop/s"] = tmplist[6]
                        throughput_info["txcarr/s"] = tmplist[7]
                        throughput_info["rxfram/s"] = tmplist[8]
                        throughput_info["rxfifo/s"] = tmplist[9]
                        throughput_info["txfifo/s"] = tmplist[10]
                        throughput_list[tmplist[1]] = throughput_info

        except IOError, e:
            logger.error(e.message, e)
            return False, throughput_list

        return True, throughput_list

    @classmethod
    def get_socket_info(cls):
        """
        get socket info
        :return:
        """
        socket_info = {}

        try:
            logger.debug("socket begin:======>")
            rtinfo = functions.launchcmd('sar -n SOCK 1 1').readlines()
            logger.debug("commands finished! ")
            if rtinfo:
                continue_falg = True
                for item in rtinfo:
                    if continue_falg:
                        if "totsck" in item:
                            continue_falg = False
                        continue
                    tmplist = item.split()
                    socket_info["time"] = tmplist[0]
                    socket_info["totsck"] = tmplist[1]
                    socket_info["tcpsck"] = tmplist[2]
                    socket_info["udpsck"] = tmplist[3]
                    socket_info["rawsck"] = tmplist[4]
                    socket_info["ip-frag"] = tmplist[5]
                    socket_info["tcp-tw"] = tmplist[6]
                    break
        except IOError, e:
            logger.error(e.message, e)
            return False, socket_info

        return True, socket_info

    @classmethod
    def get_iptrafic_info(cls):
        """
        get iptrafic info
        :return:
        """

        iptrafic_info = {}

        try:
            logger.debug("iptrafic begin:======>")
            rtinfo = functions.launchcmd('sar -n ALL 1 1').readlines()
            logger.debug("commands finished! ")
            if rtinfo:
                continue_falg = True
                falg = True
                for item in rtinfo:
                    if continue_falg:
                        if "irec" in item:
                            continue_falg = False
                        continue
                    if "ihdrerr" in item:
                        falg = False
                        continue
                    if "imsg" in item:
                        break
                    tmplist = item.split()
                    if tmplist is None or tmplist == []:
                        continue
                    if falg:
                        iptrafic_info["time"] = tmplist[0]
                        iptrafic_info["irec/s"] = tmplist[1]
                        iptrafic_info["fwddgm/s"] = tmplist[2]
                        iptrafic_info["idel/s"] = tmplist[3]
                        iptrafic_info["orq/s"] = tmplist[4]
                        iptrafic_info["asmrq/s"] = tmplist[5]
                        iptrafic_info["asmok/s"] = tmplist[6]
                        iptrafic_info["fragok/s"] = tmplist[7]
                        iptrafic_info["fragcrt/s"] = tmplist[8]
                    else:
                        iptrafic_info["ihdrerr/s"] = tmplist[1]
                        iptrafic_info["iadrerr/s"] = tmplist[2]
                        iptrafic_info["iukwnpr/s"] = tmplist[3]
                        iptrafic_info["idisc/s"] = tmplist[4]
                        iptrafic_info["odisc/s"] = tmplist[5]
                        iptrafic_info["onort/s"] = tmplist[6]
                        iptrafic_info["asmf/s"] = tmplist[7]
                        iptrafic_info["fragf/s"] = tmplist[8]

        except IOError, e:
            logger.error(e.message, e)
            return False, iptrafic_info

        return True, iptrafic_info

    @classmethod
    def get_udp_info(cls):
        """
        get udp info
        :return:
        """

        udp_info = {}

        try:
            logger.debug("udp begin:======>")
            rtinfo = functions.launchcmd('sar -n UDP 1 1').readlines()
            logger.debug("commands finished! ")
            if rtinfo:
                continue_falg = True
                for item in rtinfo:
                    if continue_falg:
                        if "idgm" in item:
                            continue_falg = False
                        continue
                    tmplist = item.split()
                    udp_info["time"] = tmplist[0]
                    udp_info["idgm/s"] = tmplist[1]
                    udp_info["odgm/s"] = tmplist[2]
                    udp_info["noport/s"] = tmplist[3]
                    udp_info["idgmerr/s"] = tmplist[4]
                    break
        except IOError, e:
            logger.error(e.message, e)
            return False, udp_info

        return True, udp_info

    @classmethod
    def get_tcp_info(cls):
        """
        get tcp info
        :return:
        """

        tcp_info = {}

        try:
            logger.debug("tcp begin:======>")
            rtinfo = functions.launchcmd('sar -n ALL 1 1').readlines()
            logger.debug("commands finished! ")
            if rtinfo:
                continue_falg = True
                falg = True
                for item in rtinfo:
                    if continue_falg:
                        if "active" in item:
                            continue_falg = False
                        continue
                    if "atmptf" in item:
                        falg = False
                        continue
                    if "idgm" in item:
                        break
                    tmplist = item.split()
                    if tmplist is None or tmplist == []:
                        continue
                    if falg:
                        tcp_info["time"] = tmplist[0]
                        tcp_info["active/s"] = tmplist[1]
                        tcp_info["passive/s"] = tmplist[2]
                        tcp_info["iseg/s"] = tmplist[3]
                        tcp_info["oseg/s"] = tmplist[4]
                    else:
                        tcp_info["atmptf/s"] = tmplist[1]
                        tcp_info["estres/s"] = tmplist[2]
                        tcp_info["retrans/s"] = tmplist[3]
                        tcp_info["isegerr/s"] = tmplist[4]
                        tcp_info["orsts/s"] = tmplist[5]
        except IOError, e:
            logger.error(e.message, e)
            return False, tcp_info

        return True, tcp_info
