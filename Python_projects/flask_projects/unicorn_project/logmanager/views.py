"""
The main module for processing the view-related tasks.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import service

__author__ = 'zhangguolei@inspur.com'


class UnicornLog(APIView):
    """
    get :get Unicorn log
    """

    def get(self, request, format=None):
        """
       get Unicorn log
        """
        retflg, retstr = service.LogDetailBusiness.view_unicornlogdetail_get()

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KernelLog(APIView):
    """
    get :get Kernel log
    """

    def get(self, request, format=None):
        """
       get Kernel log
        """
        retflg, retstr = service.LogDetailBusiness.view_kernellogdetail_get(request)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
