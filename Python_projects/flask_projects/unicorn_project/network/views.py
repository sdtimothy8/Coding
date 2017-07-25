#!/usr/bin/env python
# coding=utf-8

import commands
import dbus
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import conststr
import NetworkManager
import nm_common
c = NetworkManager.const

__author__ = 'liushaolin@inspur.com'


class DeviceList(APIView):
    """
    Get network device info and activate or deactivate chosen devices
    """
    def get(self, request, format=None):
        """
        Get network device info
        :param request:
        :param format:
        :return:
        """
        dlist = self.get_devices(request)
        return Response(dlist, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Change the state of a device or connection
        :param request:
        :param format:
        :return:
        """
        req_dict = request.data
        result = self.change_state(req_dict)
        if result[conststr.RET_CODE] != 0:
            return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result[conststr.RET_MSG], status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        Delete a connection
        :param request:
        :param format:
        :return:
        """
        result = {}
        req_dict = request.data
        connectionId = req_dict['Uuid']
        try:
            conn = NetworkManager.Settings.GetConnectionByUuid(connectionId)
        except dbus.exceptions.DBusException, reason:
            result[conststr.RET_TYPE] = conststr.FAILED_RES
            result[conststr.RET_MSG] = str(reason).split(':')[-1]
            result[conststr.RET_CODE] = -1
            return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        conn.Delete()
        result[conststr.RET_TYPE] = conststr.SUCCESS_RES
        result[conststr.RET_MSG] = conststr.DELETE_SUCCESS_RES
        result[conststr.RET_CODE] = 0
        return Response(result[conststr.RET_MSG], status=status.HTTP_200_OK)

    def get_devices(self, req):
        """
        Get device and connections basic information.
        :param req:
        :return:
        """
        values = req.META
        # Get http host address from meta information
        http_host = values['REMOTE_ADDR']
        devices_dict = {'Devices': []}

        for dev in NetworkManager.NetworkManager.GetDevices():
            # Get ethernet device information
            if c('device_type', dev.DeviceType) == 'ethernet':
                deviceInfo = nm_common.get_ethernet_info(dev, http_host)
                devices_dict['Devices'].append(deviceInfo)
            # Get loopback information
            if c('device_type', dev.DeviceType) == 'generic' and dev.Interface == 'lo':
                deviceInfo = nm_common.get_lo_info(dev, http_host)
                devices_dict['Devices'].append(deviceInfo)
        return devices_dict

    def change_state(self, operation):
        """
        Activate or deactivate a network device or connection
        :param operation:
        :return:
        """
        result = {}
        deviceId = operation['DevName']
        try:
            dev = NetworkManager.NetworkManager.GetDeviceByIpIface(deviceId)
        except dbus.exceptions.DBusException, reason:
            result[conststr.RET_TYPE] = conststr.FAILED_RES
            result[conststr.RET_MSG] = str(reason).split(':')[-1]
            result[conststr.RET_CODE] = -1
            return result
        # Activate or deactivate a device/connection
        if operation['Label'] == 'device':
            if operation['Action'] == 'activate':
                cmd = conststr.ACTIVATE_DEVICE_CMD
            else:
                cmd = conststr.DEACTIVATE_DEVICE_CMD
            cmd = cmd % deviceId
            (code, res) = commands.getstatusoutput(cmd)
            if code != 0:
                result[conststr.RET_TYPE] = conststr.FAILED_RES
                result[conststr.RET_MSG] = res
                result[conststr.RET_CODE] = code
            else:
                result[conststr.RET_TYPE] = conststr.SUCCESS_RES
                result[conststr.RET_MSG] = conststr.CHANGE_SUCCESS_RES
                result[conststr.RET_CODE] = 0
        elif operation['Label'] == 'connection':
            connectionId = operation['Uuid']
            try:
                conn = NetworkManager.Settings.GetConnectionByUuid(connectionId)
            except dbus.exceptions.DBusException, reason:
                result[conststr.RET_TYPE] = conststr.FAILED_RES
                result[conststr.RET_MSG] = str(reason).split(':')[-1]
                result[conststr.RET_CODE] = -1
                return result
            if operation['Action'] == 'activate':
                try:
                    NetworkManager.NetworkManager.ActivateConnection(conn, dev, '/')
                except dbus.exceptions.DBusException, reason:
                    result[conststr.RET_TYPE] = conststr.FAILED_RES
                    result[conststr.RET_MSG] = str(reason).split(':')[-1]
                    result[conststr.RET_CODE] = -1
                    return result
            else:
                try:
                    NetworkManager.NetworkManager.DeactivateConnection(conn)
                except dbus.exceptions.DBusException, reason:
                    result[conststr.RET_TYPE] = conststr.FAILED_RES
                    result[conststr.RET_MSG] = str(reason).split(':')[-1]
                    result[conststr.RET_CODE] = -1
                    return result
            result[conststr.RET_TYPE] = conststr.SUCCESS_RES
            result[conststr.RET_MSG] = conststr.CHANGE_SUCCESS_RES
            result[conststr.RET_CODE] = 0
        return result


class AddConnection(APIView):
    """
    Add a new connection for a device
    """
    def get(self, request, format=None):
        """
        Get mac address list
        :param request:
        :param format:
        :return:
        """
        mac_address_dict = {'mac-addresses': []}
        mac_address_list = nm_common.get_macs()
        mac_address_dict['mac-addresses'] = mac_address_list
        return Response(mac_address_dict, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Add a wired connection
        :param request:
        :param format:
        :return:
        """
        result = {}
        connection_info = request.data
        new_connection = {
            '802-3-ethernet': {},
            'connection': {},
            'ipv4': {},
            'ipv6': {},
        }
        connectionId = str(uuid.uuid4())

        if connection_info['Identity']:
            (info_802_3, result) = nm_common.get_802_3_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            new_connection['802-3-ethernet'] = info_802_3
            connection = nm_common.get_connection_info(connectionId, **connection_info)
            new_connection['connection'] = connection
        if connection_info['IPv4']:
            (ipv4_info, result) = nm_common.get_ipv4_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            new_connection['ipv4'] = ipv4_info
        if connection_info['IPv6']:
            (ipv6_info, result) = nm_common.get_ipv6_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            new_connection['ipv6'] = ipv6_info
        NetworkManager.Settings.AddConnection(new_connection)
        result[conststr.RET_TYPE] = conststr.SUCCESS_RES
        result[conststr.RET_MSG] = conststr.ADD_SUCCESS_RES
        result[conststr.RET_CODE] = 0
        return Response(result[conststr.RET_MSG], status=status.HTTP_200_OK)


class ConnectionDetail(APIView):
    """
    Modify configure information of a connection
    """
    def get(self, request, uuid, format=None):
        """
        Get details of a connection,include identity,IPv4,IPv6 information.
        :param request:
        :param uuid:the id of a connection
        :param format:
        :return:
        """
        connectionId = uuid
        conn = NetworkManager.Settings.GetConnectionByUuid(connectionId)
        settings = conn.GetSettings()
        connection_info = {
            'Identity': {},
            'IPv4': {},
            'IPv6': {},
        }
        mac_address_list = nm_common.get_macs()
        connection_info['Identity']['mac-address-list'] = mac_address_list
        if settings['802-3-ethernet']:
            if 'mac-address' in settings['802-3-ethernet']:
                mac_address = settings['802-3-ethernet']['mac-address']
                name = [x['name'] for x in mac_address_list if x['mac-address'] == mac_address][0]
                connection_info['Identity']['mac-address'] = {'name': name, 'mac-address': mac_address}
            else:
                connection_info['Identity']['mac-address'] = ''
            if 'cloned-mac-address' in settings['802-3-ethernet']:
                connection_info['Identity']['cloned-mac-address'] = settings['802-3-ethernet']['cloned-mac-address']
            else:
                connection_info['Identity']['cloned-mac-address'] = ''
            if 'mtu' in settings['802-3-ethernet']:
                connection_info['Identity']['mtu'] = settings['802-3-ethernet']['mtu']
            else:
                connection_info['Identity']['mtu'] = 0
        if settings['connection']:
            connection_info['Identity']['name'] = settings['connection']['id']
            if 'permissions' in settings['connection'] and settings['connection']['permissions']:
                connection_info['Identity']['permissions'] = False
            else:
                connection_info['Identity']['permissions'] = True
            if 'autoconnect' in settings['connection']:
                connection_info['Identity']['autoconnect'] = False
            else:
                connection_info['Identity']['autoconnect'] = True
        if settings['ipv4']:
            if settings['ipv4']['addresses']:
                connection_info['IPv4']['addresses'] = settings['ipv4']['addresses']
            else:
                connection_info['IPv4']['addresses'] = ''
            if settings['ipv4']['dns']:
                connection_info['IPv4']['dns'] = settings['ipv4']['dns']
            else:
                connection_info['IPv4']['dns'] = ''
            if settings['ipv4']['method']:
                connection_info['IPv4']['method'] = settings['ipv4']['method']
            if 'ignore-auto-dns' in settings['ipv4']:
                connection_info['IPv4']['ignore-auto-dns'] = True
            else:
                connection_info['IPv4']['ignore-auto-dns'] = False
            if 'never-default' in settings['ipv4']:
                connection_info['IPv4']['never-default'] = True
            else:
                connection_info['IPv4']['never-default'] = False
        if settings['ipv6']:
            if settings['ipv6']['addresses']:
                connection_info['IPv6']['addresses'] = settings['ipv6']['addresses']
            else:
                connection_info['IPv6']['addresses'] = ''
            if settings['ipv6']['dns']:
                connection_info['IPv6']['dns'] = settings['ipv6']['dns']
            else:
                connection_info['IPv6']['dns'] = ''
            if settings['ipv6']['method']:
                connection_info['IPv6']['method'] = settings['ipv6']['method']
            if 'ignore-auto-dns' in settings['ipv6']:
                connection_info['IPv6']['ignore-auto-dns'] = True
            else:
                connection_info['IPv6']['ignore-auto-dns'] = False
            if 'never-default' in settings['ipv6']:
                connection_info['IPv6']['never-default'] = True
            else:
                connection_info['IPv6']['never-default'] = False

        return Response(connection_info, status=status.HTTP_200_OK)

    def post(self, request, uuid, format=None):
        """
        Reset the configure information of a connection
        :param request:
        :param uuid:the id of a connection
        :param format:
        :return:
        """
        connection_info = request.data
        name = connection_info['Identity']['name']
        result = {}
        connectionId = uuid
        conn = NetworkManager.Settings.GetConnectionByUuid(connectionId)
        settings = conn.GetSettings()
        update_connection = {
            '802-3-ethernet': {},
            'connection': {},
            'ipv4': {},
            'ipv6': {},
        }
        if 'mac-address' in settings['802-3-ethernet']:
            update_connection['802-3-ethernet']['mac-address'] = settings['802-3-ethernet']['mac-address']
        update_connection['connection']['uuid'] = connectionId
        update_connection['connection']['id'] = name
        update_connection['connection']['type'] = '802-3-ethernet'
        update_connection['ipv4'] = {'method': 'auto'}
        update_connection['ipv6'] = {'method': 'auto'}
        conn.Update(update_connection)
        result[conststr.RET_TYPE] = conststr.SUCCESS_RES
        result[conststr.RET_MSG] = conststr.RESET_SUCCESS_RES
        result[conststr.RET_CODE] = 0
        return Response(result[conststr.RET_MSG], status=status.HTTP_200_OK)

    def put(self, request, uuid, format=None):
        """
        Update the configure information of a connection
        :param request:
        :param uuid:the id of a connection
        :param format:
        :return:
        """
        result = {}
        connection_info = request.data
        connectionId = uuid
        update_connection = {
            '802-3-ethernet': {},
            'connection': {},
            'ipv4': {},
            'ipv6': {},
        }
        if connection_info['Identity']:
            (info_802_3, result) = nm_common.get_802_3_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_connection['802-3-ethernet'] = info_802_3
            connection = nm_common.get_connection_info(connectionId, **connection_info)
            update_connection['connection'] = connection
        if connection_info['IPv4']:
            (ipv4_info, result) = nm_common.get_ipv4_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_connection['ipv4'] = ipv4_info
        if connection_info['IPv6']:
            (ipv6_info, result) = nm_common.get_ipv6_info(**connection_info)
            if result:
                return Response(result[conststr.RET_MSG], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            update_connection['ipv6'] = ipv6_info
        conn = NetworkManager.Settings.GetConnectionByUuid(connectionId)
        conn.Update(update_connection)
        result[conststr.RET_TYPE] = conststr.SUCCESS_RES
        result[conststr.RET_MSG] = conststr.UPDATE_SUCCESS_RES
        result[conststr.RET_CODE] = 0
        return Response(result[conststr.RET_MSG], status=status.HTTP_200_OK)
