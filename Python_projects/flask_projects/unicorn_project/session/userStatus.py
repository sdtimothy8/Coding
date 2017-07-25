'''
this module is used for locking/unlocking Users login.
'''

import time
from models import Users
from django.conf import settings


def initUserStatus(username):
    try:
        uname = Users.objects.get(username=username)
    except Users.objects.model.DoesNotExist:
        uname = Users(username=username, access_time=time.time(), try_times=0)
        uname.save()
    else:
        uname.access_time = time.time()
        uname.try_times = 0
        uname.save()


def updateUserStatus(username, access_time):
    try:
        uname = Users.objects.get(username=username)
    except Users.objects.model.DoesNotExist:
        return False
    else:
        uname.access_time = access_time
        uname.try_times = uname.try_times + 1
        uname.save()
    return True


def getLastAccessTime(username):
    try:
        uname = Users.objects.get(username=username)
    except Users.objects.model.DoesNotExist:
        return None
    return uname.access_time


def getUserStatus(username):
    try:
        uname = Users.objects.get(username=username)
    except Users.objects.model.DoesNotExist:
        uname = 0
    return uname.try_times


def isUserLocked(username):
    if isinstance(username, str):
        try_times = getUserStatus(username)
    else:
        raise TypeError
    if isinstance(try_times, int) and try_times >= settings.TRY_TIMES:
        return True
    return False


def isUserExist(username):
    try:
        uname = Users.objects.get(username=username)
    except Users.objects.model.DoesNotExist:
        return False
    else:
        return True
