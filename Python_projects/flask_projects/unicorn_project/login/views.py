'''
this module is used to:
login class: for root users' login
logoff class: for root users' logout
validateCode: 1. creating string code images and
              2. for users' validating code images in web html
'''

import random
import StringIO as StringIO
from django.http import Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from session.permission import KSMP_Permission
import session.SessionAuthticateMiddleWare
from public import functions


class Login(APIView):
    '''
    for unicorn users' login proceed.
    '''

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, Request, format=None):
        '''
           post method
        '''
        data = Request.data
        try:
            username = data['username']
            password = data['password']
            username = functions.unicorn_decrypt(data['username'])
            password = functions.unicorn_decrypt(data['password'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if not session.SessionAuthticateMiddleWare.isvalid(username, password):
                return Response(status=status.HTTP_404_NOT_FOUND)

        if Request.isPermissioned:

            retcode = [{
                        "status": "success",
                        "message": "login success"
                       }]

        else:
            retcode = [{
                        "status": "fail",
                        "message": "login fail"
                        }]

        return Response(retcode, status=status.HTTP_200_OK)


class Logoff(APIView):
    '''
    logoff view
    '''
    def post(self, request, format=None):
        '''
        post method for logined users' logoff
        '''
        try:
            auth = request.COOKIES[settings.SESSION_COOKIE_NAME]
        except KeyError:
            return Response(data="never login.", status=status.HTTP_200_OK)

        permission = KSMP_Permission()
        try:
            pms = permission.get_permission(auth)
        except TypeError:
            pms = None

        if pms:
            try:
                permission.delete_auth(pms)
            except Exception as e:
                return Response(data="logout fail.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data="logout success.", status=status.HTTP_200_OK)
