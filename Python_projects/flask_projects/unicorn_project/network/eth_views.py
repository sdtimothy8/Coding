#!/usr/bin/env python
# coding=utf-8
import NetworkManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
c = NetworkManager.const

__author__ = 'liushaolin@inspur.com'


class EthNameList(APIView):
    """
    Get a ethernet device name list.
    """
    def get(self, request):
        """
        Get  ethernet device name
        """
        ethnames = [dev.Interface for dev in NetworkManager.NetworkManager.GetDevices() if c('device_type', dev.DeviceType) == 'ethernet']
        return Response(ethnames, status=status.HTTP_200_OK)
