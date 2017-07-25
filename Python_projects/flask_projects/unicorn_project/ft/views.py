"""
The main module for processing the view-related tasks.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import service
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# import logging
# logging.basicConfig(filename='/var/log/ksmp_ft.log', level=logging.DEBUG)
# logging.debug("***sys.getdefaultencoding = " + sys.getdefaultencoding())

__author__ = 'yuxiubj@inspur.com'


class FTList(APIView):
    """
    post:upload file
    get :get list for dir
    """

    def post(self, request, format=None):
        """
        post:upload file
        """

        retflg, retstr = service.FileBusiness.upload_file_post(request)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        """
        list for dir
        """
        retflg, retstr = service.FileBusiness.ft_dir_list_get(request)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FTDetail(APIView):
    """
    operate one file
    get   :download file
    """
    def get(self, request, itemid, format=None):
        """
        download file
        """
        retflg, retstr = service.FileDetailBusiness.download_file_get(request, itemid)

        if retflg:
            return retstr
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
