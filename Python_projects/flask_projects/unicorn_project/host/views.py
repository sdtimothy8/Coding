"""
The module for host related features.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import socket

__author__ = 'caofengbing@inspur.com'
# Create your views here.


class HostList(APIView):
    """
    List all host items, or create a new one.
    ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
    """
    def get(self, request, format=None):
        """
        Get host list.
        """
        host_list = []
        host_lines = open('/etc/hosts').readlines()
        try:
            for line in host_lines:
                one_line = line.split()
                if len(one_line) == 0:
                    continue
                ip = one_line[0]
                if ip.find("#") == -1:
                    hostname = ' '.join(one_line[1: len(one_line)])
                    one_host = {'ip': ip, 'hostname': hostname}
                    host_list.append(one_host)
            return Response(host_list, status=status.HTTP_200_OK)
        except IOError as err:
                return Response("file error"+str(err), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """
        1,Create one new host
        """
        data = request.DATA
        ip = data.get('ip')
        hostname = data.get('hostname')
        if valid_ip(ip):
            if exist_ip(ip):
                return Response('This host ip is exist!', status=status.HTTP_400_BAD_REQUEST)
            else:
                host_output = open('/etc/hosts', 'a')
                try:
                    insert_info = ip+'   '+hostname+'\n'
                    host_output.write(insert_info)
                    return Response('Add host success!', status=status.HTTP_200_OK)
                except IOError as err:
                    return Response("file error"+str(err), status=status.HTTP_400_BAD_REQUEST)
                finally:
                    host_output.close()
        else:
            Response('This ip is invalid!', status=status.HTTP_400_BAD_REQUEST)

        return Response(ip+hostname, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        # host_ip = request.GET.get('ip', None)

        host_ip = request.data.get('ip')
        ip_list = host_ip.split(',')
        if len(ip_list):
            delete_host(ip_list)
            return Response('Delete success !', status=status.HTTP_200_OK)
        else:
            return Response('This ip list is empty!', status.HTTP_400_BAD_REQUEST)


def delete_host(ip_list):
    """
    delete the selected host items
    :param ip_list:
    :return:
    """
    host_list = []
    host_output = open('/etc/hosts').readlines()
    for host_line in host_output:
        ip_line = host_line.split()
        if len(ip_line) == 0:
            continue
        ip = ip_line[0]
        if ip_list.count(ip) == 0:
            host_list.append(host_line)

    if len(host_list):
        host_file = open('/etc/hosts', 'w+')
        try:
            host_file.writelines(host_list)
            host_file.close()
        except IOError:
            return Response("file error", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Unknown error!', status.HTTP_500_INTERNAL_SERVER_ERROR)


def valid_ip(address):
    """
    check the ip address
    :param address:
    :return:
    """
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def exist_ip(address):
    """
    check ip is exist in the /etc/hosts file
    :param address:
    :return:
    """
    host_lines = open('/etc/hosts').readlines()
    flag = False
    for line in host_lines:
        one_line = line.split()
        if len(one_line) == 0:
            continue
        ip = one_line[0]
        if ip == address:
            flag = True
    return flag
