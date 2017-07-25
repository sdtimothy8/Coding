#!/usr/bin/env python
# coding=utf-8

import re
from . import conststr
import NetworkManager
c = NetworkManager.const

__author__ = 'liushaolin@inspur.com'

IPV4_PATTERN = '^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
IPV6_PATTERN = '^([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4}$' \
               '|^:((:[\da-fA-F]{1,4}){1,6}|:)$' \
               '|^[\da-fA-F]{1,4}:((:[\da-fA-F]{1,4}){1,5}' \
               '|:)$|^([\da-fA-F]{1,4}:){2}((:[\da-fA-F]{1,4}){1,4}|:)$' \
               '|^([\da-fA-F]{1,4}:){3}((:[\da-fA-F]{1,4}){1,3}|:)$' \
               '|^([\da-fA-F]{1,4}:){4}((:[\da-fA-F]{1,4}){1,2}|:)$' \
               '|^([\da-fA-F]{1,4}:){5}:([\da-fA-F]{1,4})?$|^([\da-fA-F]{1,4}:){6}:$'
MAC_PATTERN = '^([0-9A-F]{2}:){5}[0-9A-F]{2}$'


def get_macs():
    """
    Get mac address of available devices
    :return:
    """
    mac_address_list = []
    for dev in NetworkManager.NetworkManager.GetDevices():
        if c('device_type', dev.DeviceType) == 'ethernet' and c('device_state', dev.State) != 'unavailable':
            mac_info = {'name': dev.Interface, 'mac-address': dev.SpecificDevice().PermHwAddress}
            mac_address_list.append(mac_info)
    return mac_address_list


def check_ipv4(*ips):
    """
    Check if ipv4 address is valid
    :param ips:ipv4 address list
    :return:
    """
    for ip in ips:
        if not re.match(IPV4_PATTERN, ip):
            return False
    return True


def check_ipv6(*ips):
    """
    Check if ipv6 address is valid
    :param ips:ipv6 address list
    :return:
    """
    for ip in ips:
        if not re.match(IPV6_PATTERN, ip):
            return False
    return True


def check_pf4(*pfs):
    """
    Check if ipv4 prefix is valid
    :param pfs:ipv4 prefix list
    :return:
    """
    for pf in pfs:
        if not isinstance(pf, int):
            return False
        elif pf < 1 or pf > 32:
            return False
    return True


def check_pf6(*pfs):
    """
    Check if ipv6 prefix is valid
    :param pfs:ipv6 prefix list
    :return:
    """
    for pf in pfs:
        if not isinstance(pf, int):
            return False
        elif pf < 1 or pf > 128:
            return False
    return True


def check_mac(mac):
    """
    Check if mac address is valid
    :param mac:mac address
    :return:
    """
    if re.match(MAC_PATTERN, mac):
        return True
    else:
        return False


def get_active_conns():
    """
    Get active connection list
    :return:
    """
    active_connections = []
    for conn in NetworkManager.NetworkManager.ActiveConnections:
        active_connections.append(conn.Uuid)
    return active_connections


def get_active_by_uuid(uuid):
    for conn in NetworkManager.NetworkManager.ActiveConnections:
        if conn.Uuid == uuid:
            return conn    # Once an uuid matched,return the connection object.
    return 0               # If no uuid is matched,return '0' to indicate this connection is not active.


def dev_own_conn(dev, conn):
    """
    Check if dev owns conn.conn is an acvite connection.
    :param dev:
    :param conn:
    :return:
    """
    for x in conn.Devices:
        if x.Interface == dev.Interface:
            return True
        else:
            return False


def get_ethernet_info(dev, http_host):
    """
    Get ethernet device information
    :param dev:dev represent a device object
    :param http_host:
    :return:
    """
    active_connections = get_active_conns()
    deviceInfo = {
        'DevName': dev.Interface,
        'DevType': c('device_type', dev.DeviceType),
        'DevState': c('device_state', dev.State),
        'Speed': '',
        'Connections': [],
        'Connected': False,
    }

    for conn in dev.AvailableConnections:
        connectionInfo = {
            'Name': '',
            'Type': '',
            'Uuid': '',
            'Detail': {
                'Ipv4_Addr': '',
                'Ipv6_Addr': '',
                'HwAddr': '',
                'Default_Route': '',
                'Nameservers': '',
            },
        }
        g_settings = conn.GetSettings()
        settings = g_settings['connection']
        connectionId = settings['uuid']
        connectionInfo['Name'] = settings['id']
        connectionInfo['Type'] = settings['type']
        connectionInfo['Uuid'] = connectionId
        conn = get_active_by_uuid(connectionId)
        # Check if an active connection belongs to a device.
        if conn and dev_own_conn(dev, conn):
            connectionInfo['State'] = 'UP'
            deviceInfo['Speed'] = str(dev.SpecificDevice().Speed)+'Mb/s'
            try:
                connectionInfo['Detail']['Ipv4_Addr'] = dev.Ip4Config.Addresses[0][0]
            except:
                connectionInfo['Detail']['Ipv4_Addr'] = ''
            try:
                connectionInfo['Detail']['Ipv6_Addr'] = dev.Ip6Config.Addresses[0][0]
            except:
                connectionInfo['Detail']['Ipv6_Addr'] = ''
            connectionInfo['Detail']['HwAddr'] = dev.SpecificDevice().HwAddress
            try:
                connectionInfo['Detail']['Default_Route'] = dev.Ip4Config.Addresses[0][2]
            except:
                connectionInfo['Detail']['Default_Route'] = ''
            try:
                connectionInfo['Detail']['Nameservers'] = ' '.join(dev.Ip4Config.Nameservers)
            except:
                connectionInfo['Detail']['Nameservers'] = ''
        else:
            connectionInfo['State'] = 'DOWN'

        deviceInfo['Connections'].append(connectionInfo)
        if connectionInfo['Detail']['Ipv4_Addr'] == http_host:
            deviceInfo['Connected'] = True
    return deviceInfo


def get_lo_info(dev, http_host):
    """
    Get loopback device information
    :param dev:dev represent a device object
    :param http_host:
    :return:
    """
    active_connections = get_active_conns()
    deviceInfo = {
        'DevName': dev.Interface,
        'DevType': c('device_type', dev.DeviceType),
        'DevState': c('device_state', dev.State),
        'Speed': '',
        'Connections': [],
        'Connected': False,
    }
    connectionInfo = {
        'Name': '',
        'Type': '',
        'Uuid': '',
        'Detail': {
            'Ipv4_Addr': '',
            'Ipv6_Addr': '',
            'HwAddr': '',
        },
    }
    try:
        connectionInfo['Detail']['Ipv4_Addr'] = dev.Ip4Config.Addresses[0][0]
    except:
        connectionInfo['Detail']['Ipv4_Addr'] = ''
    try:
        connectionInfo['Detail']['Ipv6_Addr'] = dev.Ip6Config.Addresses[0][0]
    except:
        connectionInfo['Detail']['Ipv6_Addr'] = ''
    connectionInfo['Detail']['HwAddr'] = '00:00:00:00:00:00'
    deviceInfo['Connections'].append(connectionInfo)
    if connectionInfo['Detail']['Ipv4_Addr'] == http_host:
        deviceInfo['Connected'] = True
    return deviceInfo


def get_802_3_info(**connection_info):
    """
    Get 802-3-ethernet information when add or update a connection
    :param connection_info:
    :return:
    """
    info_802_3 = {}
    res = {}
    if connection_info['Identity']['mac-address']:
        info_802_3['mac-address'] = connection_info['Identity']['mac-address']
    if connection_info['Identity']['cloned-mac-address']:
        # Check if cloned-mac-address is valid
        if check_mac(connection_info['Identity']['cloned-mac-address']):
            info_802_3['cloned-mac-address'] = connection_info['Identity']['cloned-mac-address']
        else:
            res[conststr.RET_TYPE] = conststr.FAILED_RES
            res[conststr.RET_MSG] = conststr.INVALID_MAC_ADDR
            res[conststr.RET_CODE] = -1
    if connection_info['Identity']['mtu']:
        info_802_3['mtu'] = connection_info['Identity']['mtu']
    return info_802_3, res


def get_connection_info(connectionId, **connection_info):
    """
    Get connection information when add or update a connection
    :param connectionId:
    :param connection_info:
    :return:
    """
    connection = {}
    connection['type'] = '802-3-ethernet'
    connection['uuid'] = connectionId
    if connection_info['Identity']['name']:
        connection['id'] = connection_info['Identity']['name']
    if connection_info['Identity']['autoconnect']:
        connection['autoconnect'] = True
    else:
        connection['autoconnect'] = False
    if not connection_info['Identity']['permissions']:
        connection['permissions'] = ['user:root:']
    return connection


def get_ipv4_info(**connection_info):
    """
    Get ipv4 information when add or update a connection
    :param connection_info:
    :return:
    """
    ipv4_info = {}
    res = {}
    if connection_info['IPv4']['method'] == 'auto':
        ipv4_info['method'] = 'auto'
        if connection_info['IPv4']['ignore-auto-dns']:
            ipv4_info['ignore-auto-dns'] = connection_info['IPv4']['ignore-auto-dns']
        if connection_info['IPv4']['never-default']:
            ipv4_info['never-default'] = connection_info['IPv4']['never-default']
        if connection_info['IPv4']['dns']:
            # Check if dns is valid
            if check_ipv4(*connection_info['IPv4']['dns']):
                ipv4_info['dns'] = connection_info['IPv4']['dns']
            else:
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_DNS_ADDR
                res[conststr.RET_CODE] = -1
    elif connection_info['IPv4']['method'] == 'manual':
        ipv4_info['method'] = 'manual'
        if connection_info['IPv4']['addresses']:
            # Check if ipv4 address is valid.
            ips = [x[0] for x in connection_info['IPv4']['addresses']] + [x[2] for x in connection_info['IPv4']['addresses']]
            pfs = [x[1] for x in connection_info['IPv4']['addresses']]
            if not check_ipv4(*ips):
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_IPV4_ADDR
                res[conststr.RET_CODE] = -1
            elif not check_pf4(*pfs):
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_IPV4_PREFIX
                res[conststr.RET_CODE] = -1
            else:
                ipv4_info['addresses'] = connection_info['IPv4']['addresses']
        else:
            res[conststr.RET_TYPE] = conststr.FAILED_RES
            res[conststr.RET_MSG] = conststr.EMPTY_IPV4_ADDR
            res[conststr.RET_CODE] = -1
        if connection_info['IPv4']['dns']:
            # Check if dns is valid
            if check_ipv4(*connection_info['IPv4']['dns']):
                ipv4_info['dns'] = connection_info['IPv4']['dns']
            else:
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_DNS_ADDR
                res[conststr.RET_CODE] = -1
        if connection_info['IPv4']['ignore-auto-dns']:
            ipv4_info['ignore-auto-dns'] = connection_info['IPv4']['ignore-auto-dns']
        if connection_info['IPv4']['never-default']:
            ipv4_info['never-default'] = connection_info['IPv4']['never-default']
    elif connection_info['IPv4']['method'] == 'link-local':
        ipv4_info['method'] = 'link-local'
        if connection_info['IPv4']['ignore-auto-dns']:
            ipv4_info['ignore-auto-dns'] = connection_info['IPv4']['ignore-auto-dns']
        if connection_info['IPv4']['never-default']:
            ipv4_info['never-default'] = connection_info['IPv4']['never-default']
    elif connection_info['IPv4']['method'] == 'disabled':
        ipv4_info['method'] = 'disabled'
    return ipv4_info, res


def get_ipv6_info(**connection_info):
    """
    Get ipv6 information when add or update a connection
    :param connection_info:
    :return:
    """
    ipv6_info = {}
    res = {}
    if connection_info['IPv6']['method'] == 'auto' or connection_info['IPv6']['method'] == 'dhcp':
        ipv6_info['method'] = connection_info['IPv6']['method']
        if connection_info['IPv6']['ignore-auto-dns']:
            ipv6_info['ignore-auto-dns'] = connection_info['IPv6']['ignore-auto-dns']
        if connection_info['IPv6']['never-default']:
            ipv6_info['never-default'] = connection_info['IPv6']['never-default']
        if connection_info['IPv6']['dns']:
            # Check if dns is valid
            if check_ipv6(*connection_info['IPv6']['dns']):
                ipv6_info['dns'] = connection_info['IPv6']['dns']
            else:
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_DNS_ADDR
                res[conststr.RET_CODE] = -1
    elif connection_info['IPv6']['method'] == 'manual':
        ipv6_info['method'] = 'manual'
        if connection_info['IPv6']['addresses']:
            # Check if ipv6 address is valid.
            ips = [x[0] for x in connection_info['IPv6']['addresses']] + [x[2] for x in connection_info['IPv6']['addresses']]
            pfs = [x[1] for x in connection_info['IPv6']['addresses']]
            if not check_ipv6(*ips):
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_IPV6_ADDR
                res[conststr.RET_CODE] = -1
            elif not check_pf6(*pfs):
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_IPV6_PREFIX
                res[conststr.RET_CODE] = -1
            else:
                ipv6_info['addresses'] = connection_info['IPv6']['addresses']
        else:
            res[conststr.RET_TYPE] = conststr.FAILED_RES
            res[conststr.RET_MSG] = conststr.EMPTY_IPV6_ADDR
            res[conststr.RET_CODE] = -1
        if connection_info['IPv6']['dns']:
            # Check if dns is valid
            if check_ipv6(*connection_info['IPv6']['dns']):
                ipv6_info['dns'] = connection_info['IPv6']['dns']
            else:
                res[conststr.RET_TYPE] = conststr.FAILED_RES
                res[conststr.RET_MSG] = conststr.INVALID_DNS_ADDR
                res[conststr.RET_CODE] = -1
        if connection_info['IPv6']['ignore-auto-dns']:
            ipv6_info['ignore-auto-dns'] = connection_info['IPv6']['ignore-auto-dns']
        if connection_info['IPv6']['never-default']:
            ipv6_info['never-default'] = connection_info['IPv6']['never-default']
    elif connection_info['IPv6']['method'] == 'link-local':
        ipv6_info['method'] = 'link-local'
        if connection_info['IPv6']['ignore-auto-dns']:
            ipv6_info['ignore-auto-dns'] = connection_info['IPv6']['ignore-auto-dns']
        if connection_info['IPv6']['never-default']:
            ipv6_info['never-default'] = connection_info['IPv6']['never-default']
    elif connection_info['IPv6']['method'] == 'ignore':
        ipv6_info['method'] = 'ignore'
    return ipv6_info, res
