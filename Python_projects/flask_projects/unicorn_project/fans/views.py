"""
Get fans info
"""
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import os
import string


class fans(APIView):
    """
    Get fans info
    ['get']
    """

    def get(self, request, format=None):

        (code, resultMSG) = commands.getstatusoutput('ipmitool -I open sensor list')
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        fanlist = {"fans": []}

        line = resultMSG.split('\n')
        for i in range(len(line)):
            tmp = line[i].split('|')
            tmpdict = {}
            date = tmp[0]
            if date.find('FAN') != -1:
                tmpdict['fanname'] = tmp[0].strip()
                tmpdict['fanspeed'] = tmp[1].strip()
                fanlist['fans'].append(tmpdict)
        return Response(fanlist['fans'], status=status.HTTP_200_OK)
