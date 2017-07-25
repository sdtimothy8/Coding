# coding=utf-8
from util import launchcmd, getAgentId
import subprocess


def get_network_io():
    netinfo = {}
    commands_net = "sar -n DEV 1 1"
    flag, node_id = getAgentId()
    try:
        net_info_list = subprocess.Popen(commands_net, stdout=subprocess.PIPE, shell=True).stdout.readlines()
        rx = 0
        tx = 0
        for net_info in net_info_list:
            if -1 != net_info.find("：") or -1 != net_info.find(":"):
                if -1 == net_info.find("rxkB"):
                    rx = rx + float(net_info.split()[4])
                    tx = tx + float(net_info.split()[5])
        netinfo["rx"] = rx
        netinfo["tx"] = tx
        netinfo["id"] = node_id
        return netinfo
    except:
        return None


def get_throughput_info():
        """
        get throughput info
        :return:
        """

        throughput_list = {}
        flag, node_id = getAgentId()
        throughput_list["id"] = node_id
        try:

            rtinfo = launchcmd('sar -n ALL 1 1').readlines()
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

            return throughput_list

        return throughput_list


def get_socket_info():
        """
        get socket info
        :return:
        """
        socket_info = {}
        flag, node_id = getAgentId()
        socket_info["id"] = node_id
        try:
            rtinfo = launchcmd('sar -n SOCK 1 1').readlines()
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
            return socket_info

        return socket_info


def get_iptrafic_info():
        """
        get iptrafic info
        :return:
        """

        iptrafic_info = {}
        flag, node_id = getAgentId()
        iptrafic_info["id"] = node_id
        try:
            rtinfo = launchcmd('sar -n ALL 1 1').readlines()
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
            return iptrafic_info

        return iptrafic_info


def get_udp_info():
        """
        get udp info
        :return:
        """
        udp_info = {}
        flag, node_id = getAgentId()
        udp_info["id"] = node_id
        try:

            rtinfo = launchcmd('sar -n UDP 1 1').readlines()
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
            return udp_info

        return udp_info


def get_tcp_info():
        """
        get tcp info
        :return:
        """
        tcp_info = {}
        flag, node_id = getAgentId()
        tcp_info["id"] = node_id
        try:
            rtinfo = launchcmd('sar -n ALL 1 1').readlines()
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
            return tcp_info

        return tcp_info


def get_total_network():
    result = {}
    result["throughput"] = get_throughput_info()
    result["iptraffic"] = get_iptrafic_info()
    result["tcp"] = get_tcp_info()
    result["udp"] = get_udp_info()
    result["socket"] = get_socket_info()
    result["type"] = "NETWORK"
    return result

if __name__ == "__main__":

    print get_network_io()
