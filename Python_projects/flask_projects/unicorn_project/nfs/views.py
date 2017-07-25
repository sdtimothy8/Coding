"""
NFS
"""
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import os
from public import functions
from string import strip


class checkdir(APIView):
    """
    check dir exist
    ['put',]
    """
    def post(self, request, format=None):
        nfsinfo = request.data
        result = {}
        if os.path.exists(nfsinfo['path']) == True:
            result['valid'] = True
            return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        nfsinfo = request.GET.get('path')
        result = {}
        if os.path.exists(nfsinfo) == True:
            result['valid'] = True
            return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)


class checkuid(APIView):
    """
    check uid exist
    ['put',]
    """
    def get(self, request, format=None):
        nfsinfo = request.GET.get('anonuid')
        fileobj = open('/etc/passwd')
        result = {}
        for line in fileobj:
            tmp = line.split(':')
            if nfsinfo == tmp[2]:
                result['valid'] = True
                return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        nfsinfo = request.data
        fileobj = open('/etc/passwd')
        result = {}
        for line in fileobj:
            tmp = line.split(':')
            if nfsinfo['anonuid'] == tmp[2]:
                result['valid'] = True
                return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)


class checkgid(APIView):
    """
    check gid exist
    ['put',]
    """

    def get(self, request, format=None):
        nfsinfo = request.GET.get('anongid')
        fileobj = open('/etc/group')
        result = {}
        for line in fileobj:
            tmp = line.split(':')
            if nfsinfo == tmp[2]:
                result['valid'] = True
                return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        nfsinfo = request.data
        fileobj = open('/etc/group')
        result = {}
        for line in fileobj:
            tmp = line.split(':')
            if nfsinfo['anongid'] == tmp[2]:
                result['valid'] = True
                return Response(result, status=status.HTTP_200_OK)
        result['valid'] = False
        return Response(result, status=status.HTTP_200_OK)


class checknfs(APIView):
    """
    check NFS
    ['get',]
    """
    def get(self, request, format=None):
        (code, resultMSG) = commands.getstatusoutput('systemctl start rpcbind ')
        result = {}
        if code != 0:
            result['errormsg'] = resultMSG
            result['error'] = True
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        (code, resultMSG) = commands.getstatusoutput('systemctl start nfs')
        if code != 0:
            result['errormsg'] = resultMSG
            result['error'] = True
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        (code, resultMSG) = commands.getstatusoutput('exportfs -ar')
        if code != 0:
            result['errormsg'] = resultMSG
            result['error'] = True
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result['error'] = False
        result['errormsg'] = resultMSG
        return Response(result, status=status.HTTP_200_OK)


class nfs(APIView):
    """
    Get NFS list, Modify nfs configuration file
    ['get', 'post']
    """

    def get(self, request, format=None):
        """
        Get NFS list
        """

        (code, resultMSG) = commands.getstatusoutput('exportfs -ar')
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        nfslist = {"data": []}
        file_object = open('/etc/exports')
        for line in file_object:
            tmpdict = {}
            # change '\t' to ' '
            getstr = line.replace('\t', ' ')
            # del ' ' infront of line
            getstr = getstr.lstrip()
            tmp = getstr.find(' ')
            tmpdict['dir'] = getstr[:tmp]
            tmpdict['rule'] = getstr[tmp:].strip()
            if tmpdict['dir'].find('#') == -1:
                tmpdict['switch'] = 'on'
            else:
                tmpdict['switch'] = 'off'
                tmpdict['dir'] = tmpdict['dir'][1:]
            tmpdict['line'] = line
            if tmpdict['dir'] != '' and tmpdict['rule'] != '':
                nfslist['data'].append(tmpdict)
        return Response(nfslist, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Modify nfs configuration file
        """

        nfsinfo = request.data

        if nfsinfo['cmd'] == 'add':  # add one nfs
            newnfs = '\n' + nfsinfo['line'] + '\n'
            (code, resultMSG) = commands.getstatusoutput('cp /etc/exports /etc/exports.ksmp.bak -r')
            if code != 0:
                return Response('init error!\n', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            exist_flag = check_exist(nfsinfo['line'])
            if exist_flag:
                r = open('/etc/exports')
                w = open('/etc/exports.tmp', 'w')
                for readin in r.readlines():
                    if strip(readin) == "":
                        # w.writelines(readin)
                        continue
                    newrulelist = strip(nfsinfo['line']).split()
                    newfilerulelist = strip(readin).split()
                    newrulelist[0] = strip(newrulelist[0]) if newrulelist[0].endswith('/') else "{}/".format(
                        newrulelist[0])
                    newfilerulelist[0] = strip(newfilerulelist[0]) if newfilerulelist[0].endswith(
                        '/') else "{}/".format(newfilerulelist[0])
                    newrule = " ".join(newrulelist).split('(')
                    newfileline = " ".join(newfilerulelist).split('(')
                    if newfileline[0].startswith('#') and strip(newrule[0]) == strip(newfileline[0].replace('#', '')):
                        #     return True
                        # from ksmp import logger
                        # logger.error("{}  |  {}".format(readin.replace('#', ''), nfsinfo['line']))
                        # if readin.replace('#', '') == nfsinfo['line']:
                        #     logger.error(newnfs)
                        w.writelines(newnfs)
                    else:
                        w.writelines(readin)
                r.close()
                w.close()
                (code, resultMSG) = commands.getstatusoutput('(rm /etc/exports -r) && (mv /etc/exports.tmp /etc/exports -f)')
                if code != 0:
                    return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(resultMSG, status=status.HTTP_200_OK)
            output = open('/etc/exports', 'a')
            output .write(newnfs)
            output .close()
            (code, resultMSG) = commands.getstatusoutput('exportfs -ar')
            if code != 0:
                commands.getstatusoutput('cp /etc/exports.ksmp.bak /etc/exports -r')
                return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(resultMSG, status=status.HTTP_200_OK)

        if nfsinfo['cmd'] == 'on':    # set one nfs on
            tmp = nfsinfo['line'].find('#')
            if tmp == -1:
                return Response('The nfs had turn on! \n', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                r = open('/etc/exports')
                w = open('/etc/exports.tmp', 'w')
                for readin in r.readlines():
                    if readin == nfsinfo['line']:
                        w.writelines(nfsinfo['line'].replace('#', ''))
                    else:
                        w.writelines(readin)
                r.close()
                w.close()
                (code, resultMSG) = commands.getstatusoutput('(rm /etc/exports -r) && (mv /etc/exports.tmp /etc/exports -f)')
                if code != 0:
                    return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response('turn on', status=status.HTTP_200_OK)

        if nfsinfo['cmd'] == 'off':    # set one nfs off
            tmp = nfsinfo['line'].find('#')
            if tmp == -1:
                newline = '#' + nfsinfo['line']

                r = open('/etc/exports')
                w = open('/etc/exports.tmp', 'w')
                for readin in r.readlines():
                    if readin == nfsinfo['line']:
                        w.writelines(newline)
                    else:
                        w.writelines(readin)
                r.close()
                w.close()
                (code, resultMSG) = commands.getstatusoutput('(rm /etc/exports -r) && (mv /etc/exports.tmp /etc/exports -f)')
                if code != 0:
                    return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response('turn off', status=status.HTTP_200_OK)
            else:
                return Response('The nfs had turn off! \n', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if nfsinfo['cmd'] == 'del':    # del one line
            r = open('/etc/exports')
            w = open('/etc/exports.tmp', 'w')
            for readin in r.readlines():
                if readin != nfsinfo['line']:
                    w.writelines(readin)
            r.close()
            w.close()
            (code, resultMSG) = commands.getstatusoutput('(rm /etc/exports -r) && (mv /etc/exports.tmp /etc/exports -f)')
            if code != 0:
                return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('del', status=status.HTTP_200_OK)


def check_exist(rule):
    if rule is not None:
        filterfile = functions.launchcmd("cat /etc/exports").readlines()

        for daemonline in filterfile:
            # newrule = strip(rule) if rule.endswith('/') else "{}/".format(rule)
            # newfileline = strip(daemonline) if daemonline.endswith('/') else "{}/".format(daemonline)
            if strip(daemonline) == "":
                continue
            newrulelist = strip(rule).split()
            newfilerulelist = strip(daemonline).split()
            newrulelist[0] = strip(newrulelist[0]) if newrulelist[0].endswith('/') else "{}/".format(newrulelist[0])
            newfilerulelist[0] = strip(newfilerulelist[0]) if newfilerulelist[0].endswith('/') else "{}/".format(newfilerulelist[0])
            newrule = " ".join(newrulelist).split('(')
            newfileline = " ".join(newfilerulelist).split('(')
            if daemonline.startswith('#') and strip(newrule[0]) == strip(newfileline[0].replace('#', '')):
                return True
    return False
