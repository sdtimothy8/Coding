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

__author__ = 'yuxiubj@inspur.com'


class LogList(APIView):
    """
    post:upload log file
    get :get log list for dir
    """

    def post(self, request, format=None):
        """
        upload one new log.
        """
        retflg, retstr = service.LogBusiness.upload_file_post(request)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        """
        get list for dir
        """
        retflg, retstr = service.LogBusiness.log_dir_list_get(request)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogDetail(APIView):
    """
    operate one log file
    get   :get log detail
    delete:Delete selected log
    """

    def get(self, request, itemid, format=None):
        """
        Get log detail.
        """
        retflg, retstr = service.LogDetailBusiness.view_logdetail_get(request, itemid)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, itemid, format=None):
        """
        Delete selected log.
        """
        retflg, retstr = service.LogDetailBusiness.delete_log(request, itemid)

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
