# coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import os


class fdisklist(APIView):
    """
    get fdisk driver info
    ['get']
    """

    def get(self, request, cmd):
        """
        get fdisk driver info
        """
        if cmd == 'getfdisklist':
            (code, resultMSG) = commands.getstatusoutput('df -h')
            if code != 0:
                return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            disklist = {'string': []}
            line = resultMSG.split('\n')
            for i in range(len(line)):
                tmp = line[i].split()
                tmpdict = {}
                tmpdict['Filesystem'] = tmp[0]
                tmpdict['Size'] = tmp[1]
                tmpdict['Used'] = tmp[2]
                tmpdict['Avail'] = tmp[3]
                tmpdict['Use'] = tmp[4]
                tmpdict['Mouted'] = tmp[5]
                disklist['string'].append(tmpdict)

            del disklist['string'][0]
            return Response(disklist, status=status.HTTP_200_OK)

        if cmd == 'getfdiskdriver':
            (code, resultMSG) = commands.getstatusoutput('lspci -k')
            if code != 0:
                return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            disklist = {'string': []}
            flog_find = 0
            count = 0

            line = resultMSG.split('\n')
            for i in range(len(line)):
                tmp = {}
                if flog_find == 1 and line[i][0] == '\t':
                    tmp['num'] = count
                    tmp['string'] = line[i]
                    disklist['string'].append(tmp)

                if flog_find == 1 and line[i][0] != '\t':
                    flog_find = 0
                    count = count + 1

                if flog_find == 0:
                    if 'IDE' in line[i] or 'SATA' in line[i]:
                        flog_find = 1
                        tmp['num'] = count
                        tmp['string'] = line[i]
                        disklist['string'].append(tmp)

            return Response(disklist, status=status.HTTP_200_OK)


class networklist(APIView):
    """
    get network driver information
    ['get']
    """

    def get(self, request):
        """
        get network driver information
        """
        (code, resultMSG) = commands.getstatusoutput('lshw -class network')
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        networklist = {'string': []}
        count = 0

        line = resultMSG.split('\n')
        for i in range(len(line)):
            tmp = {}
            if '*-network' in line[i]:
                count = count + 1
            tmp['num'] = count
            tmp['string'] = line[i]
            networklist['string'].append(tmp)

        return Response(networklist, status=status.HTTP_200_OK)


class pcilist(APIView):
    """
    get pci driver list
    ['get']
    """

    def get(self, request):
        """
        get pci driver list
        """
        (code, resultMSG) = commands.getstatusoutput('lspci -k')
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        pcilist = {'string': []}
        count = 0

        line = resultMSG.split('\n')
        for i in range(len(line)):
            tmp = {}
            if line[i][0] == '\t':
                tmp['num'] = count
                tmp['string'] = line[i]
                pcilist['string'].append(tmp)

            if line[i][0] != '\t':
                count = count + 1
                tmp['num'] = count
                tmp['string'] = line[i]
                pcilist['string'].append(tmp)

        return Response(pcilist, status=status.HTTP_200_OK)


class drivermodslist(APIView):
    """
    get  driver mod list
    ['get']
    """

    def get(self, request):
        """
        get  driver mod list
        """
        (code, resultMSG) = commands.getstatusoutput('lsmod')
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        modlist = {'string': []}

        line = resultMSG.split('\n')
        for i in range(len(line)):
            tmp = line[i].split()
            tmpdict = {}
            tmpdict['Module'] = tmp[0]
            tmpdict['Size'] = tmp[1]
            tmpdict['Used'] = tmp[2]
            if(len(tmp) < 4):
                tmpdict['by'] = ''
            else:
                tmpdict['by'] = tmp[3]
            modlist['string'].append(tmpdict)

        del modlist['string'][0]
        return Response(modlist, status=status.HTTP_200_OK)


class drivermodinfo(APIView):
    """
    get driver mod information by modname
    ['get']
    """
    def get(self, request, modname):
        """
        get driver mod information by modname
        """
        cmd = 'modinfo ' + modname
        (code, resultMSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        modinfo = {'string': []}
        line = resultMSG.split('\n')
        for i in range(len(line)):
            modinfo['string'].append(line[i])
        for i in range(len(modinfo['string'])):
            if "filename:" in modinfo['string'][i]:
                tmp = modinfo['string'][0]
                modinfo['string'][0] = modinfo['string'][i]
                modinfo['string'][i] = tmp
                continue
            if "license:" in modinfo['string'][i]:
                tmp = modinfo['string'][1]
                modinfo['string'][1] = modinfo['string'][i]
                modinfo['string'][i] = tmp
                continue
            if "srcversion:" in modinfo['string'][i]:
                tmp = modinfo['string'][2]
                modinfo['string'][2] = modinfo['string'][i]
                modinfo['string'][i] = tmp
                continue
            if "depends:" in modinfo['string'][i]:
                tmp = modinfo['string'][3]
                modinfo['string'][3] = modinfo['string'][i]
                modinfo['string'][i] = tmp

        return Response(modinfo, status=status.HTTP_200_OK)
