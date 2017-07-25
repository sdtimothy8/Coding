"""
this module is for TCP Wrapper views_module
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ksmp import util, message
from tcp import business

__author__ = 'zhuysh@inspur.com'

DENY_DIR = "/etc/hosts.deny"
ALLOW_DIR = "/etc/hosts.allow"


class TcpDenyList(APIView):
    """
    Tcp Wrappers deny info
    """

    def get(self, request, format=None):
        """
        GET method: Get TCP Wrapper deny list
        """

        # get tcp wrapper deny_list info
        rtn_tcplist = business.TcpBusiness.getlistinfo(DENY_DIR)

        return Response({"denyinfo": rtn_tcplist}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        POST method: add a TCP Wrapper deny_info to /etc/hosts.deny
        """

        # add tcp wrapper deny info
        rtninfo = business.TcpBusiness.putlistinfo(request, DENY_DIR)

        if "success" == rtninfo:
            return Response(util.getResult(message.RESULT_TYPE_SUCCESS, message.ADD_SUCCESS), status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, foramt=None):
        """
        DELETE method: delete selected deny_info from /etc/hosts.deny
        """

        # delete tcp wrapper deny info
        rtninfo = business.TcpBusiness.deletelistinfo(request, DENY_DIR)

        if "success" == rtninfo:
            return Response({"denyinfo": business.TcpBusiness.getlistinfo(DENY_DIR), "result": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"denyinfo": business.TcpBusiness.getlistinfo(DENY_DIR), "result": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TcpAllowList(APIView):
    """
    Tcp Wrappers allow info
    """

    def get(self, request, format=None):
        """
        GET method: Get TCP Wrapper allow list
        """

        # get tcp wrapper allow_list info
        rtn_tcplist = business.TcpBusiness.getlistinfo(ALLOW_DIR)

        return Response({"allowinfo": rtn_tcplist}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        POST method: add a TCP Wrapper deny_info to /etc/hosts.allow
        """

        # add tcp wrapper allow info
        rtninfo = business.TcpBusiness.putlistinfo(request, ALLOW_DIR)

        if "success" == rtninfo:
            return Response(util.getResult(message.RESULT_TYPE_SUCCESS, message.ADD_SUCCESS), status=status.HTTP_200_OK)
        else:
            return Response(util.getResult(message.RESULT_TYPE_ERROR, message.RESULT_TYPE_ERROR), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, foramt=None):
        """
        DELETE method: delete selected deny_info from /etc/hosts.allow
        """

        # delete tcp wrapper allow info
        rtninfo = business.TcpBusiness.deletelistinfo(request, ALLOW_DIR)

        if "success" == rtninfo:
            return Response({"allowinfo": business.TcpBusiness.getlistinfo(ALLOW_DIR), "result": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"allowinfo": business.TcpBusiness.getlistinfo(ALLOW_DIR), "result": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
