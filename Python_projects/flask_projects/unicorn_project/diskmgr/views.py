"""
The main module for processing the view-related tasks.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from diskmgr.business import DiskBusiness as DBusiness
from diskmgr import ifconfig


__author__ = 'shaomingwu@inspur.com'


class DiskMgr(APIView):
    """
    List all disks,
    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """
    def get(self, request, format=None):
        """
        GET: For disk list.
        :param request: No parameters.
        :param format:
        :return: return a dict, which contains a list, in the list, each element is a dict which corresponds to an
        disk. Just like below:
        {[{}, {}, ...]}
        """
        ret_flg, disk_dict = DBusiness.getcapacity()
        if ret_flg:
            return Response(disk_dict, status=status.HTTP_200_OK)
        else:
            return Response(ifconfig.DISK_FAILED_GETLIST, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
