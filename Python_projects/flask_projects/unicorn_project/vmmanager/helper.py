# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#
from rest_framework.response import Response
from rest_framework import status as Status

RESPONSE_SUCCESS = {"result": "success", "status": 1}
RESPONSE_DONE = {"result": "success", "status": 0, "type": "done"}
RESPONSE_NOTCHANGE = {"result": "notchange", "status": 0, "type": "notchange"}
RESPONSE_ERROR = {"result": "faild", "status": -1, "type": "error"}


def Reply(fmt=RESPONSE_DONE, data=None, status=None,
          headers=None, CROS=False):
    if fmt not in [RESPONSE_SUCCESS, RESPONSE_DONE,
                   RESPONSE_NOTCHANGE, RESPONSE_ERROR]:
        raise
    res_data = fmt.copy()
    if fmt is RESPONSE_ERROR:
        res_data["error"] = data
        status = status or Status.HTTP_400_BAD_REQUEST
    elif fmt is RESPONSE_SUCCESS:
        res_data["data"] = data
    elif fmt is RESPONSE_NOTCHANGE:
        status = status or Status.HTTP_202_ACCEPTED
    if status is None:
        status = Status.HTTP_200_OK
    if CROS:
        if headers is None:
            headers = {}
        headers["Access-Control-Allow-Origin"] = "*"
    return Response(res_data, status=status, headers=headers)
