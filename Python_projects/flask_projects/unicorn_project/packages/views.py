"""
package for user
"""
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from ksmp import util
import commands
import os
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")


class filelist(APIView):
    """
    get file lists
    """
    def get(self, request):
        info = request.GET
        dirstr = info['path']
        dirstr = dirstr.encode('utf8')
        package_dir = settings.PACKAGE_DIR
        if package_dir[-1] == '/':
            package_dir = package_dir[:-1]
        dirstr = package_dir + dirstr
        lists = os.listdir(dirstr)
        filelist = {"filelists": []}
        for line in lists:
            """
            dir must be "/home",can't be "/home/"
            """
            if dirstr[-1] != '/':
                dirstr += '/'

            if os.path.isdir(dirstr + line):
                tmpfile = {}
                tmpfile['name'] = line
                tmpfile['isdir'] = True
                filelist['filelists'].append(tmpfile)
            else:
                tmpfile = {}
                tmpfile['name'] = line
                tmpfile['isdir'] = False
                filelist['filelists'].append(tmpfile)
        # print(filelist)
        return Response(filelist, status=status.HTTP_200_OK)


class searchonepackage(APIView):
    """
    find packages with a string
    ['get']
    """

    def get(self, request):
        """
        find packages with a string
        """
        packagestr = request.GET
        packageslist = []
        cmd = "rpm -qa | grep " + packagestr['package']
        (code, resultMSG) = commands.getstatusoutput(cmd)
        if resultMSG == '':
            tempdict = {}
            tempdict['type'] = 'error'
            tempdict['info'] = 'no package equal ' + packagestr['package']
            packageslist.append(tempdict)
            return Response(packageslist, status=status.HTTP_200_OK)
        if code != 0:
            return_error = {'errormsg': resultMSG, 'errorcode': code}
            return Response(return_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        tmplist = resultMSG.split('\n')
        for onename in tmplist:
            tempdict = {}
            tempdict['type'] = 'pac'
            tempdict['info'] = onename
            packageslist.append(tempdict)

        return Response(packageslist, status=status.HTTP_200_OK)


class packages(APIView):
    """
    install packages,uninstall packages
    ['post', 'delete']
    """

    def post(self, request, format=None):
        """
        install packages
        """
        packagestr = request.data
        if packagestr['path'][-1] != '/':
            packagestr['path'] = packagestr['path'] + '/'
        package_dir = settings.PACKAGE_DIR
        if package_dir[-1] == '/':
            package_dir = package_dir[:-1]

        packagestr['path'] = package_dir + packagestr['path']
        cmd = "rpm -ivh " + packagestr['path'] + packagestr['filename']

        (code, resultMSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return_error = {'errormsg': resultMSG, 'errorcode': code}
            return Response(return_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        MSG = {'message': resultMSG}
        return_dict = {'result': MSG}

        return Response(return_dict, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        uninstall packages
        """
        packagestr = request.data

        if (packagestr['forcedel'] is not True):
            cmd = 'rpm -e ' + packagestr['package']
        else:
            cmd = 'rpm -e ' + packagestr['package'] + " --nodeps"

        (code, result) = commands.getstatusoutput(cmd)
        if code != 0:
            return_error = {'errormsg': result, 'errorcode': code}
            return Response(return_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        MSGlist = []
        MSGlist.append(packagestr['package'] + ':' + result)

        return Response(MSGlist, status=status.HTTP_200_OK)


class packageslist(APIView):
    """
    get all packages list
    ['get']
    """

    def get(self, request, url, format=None):
        """
        get all packages list
        """

        path = '/usr/share/doc/rpm-' + getRpm() + '/GROUPS'
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        # lines = ['System Environment/Libraries']
        # get first packages list
        num = url.split('/')
        len_num = 0
        for i in range(len(num)):
            if(num[i] != ''):
                len_num = len_num + 1
        if num[0] == 'all':
            len_num = 0
        tree = []
        treelist = []
        for i in range(len(lines)):
            tmp = lines[i].strip()
            tmp = tmp.split('/')

            if len_num == 0:
                if tmp[0] not in treelist:
                    tmpdict = {}
                    tmpdict["type"] = "group"
                    tmpdict["info"] = tmp[0]
                    tree.append(tmpdict)
                    treelist.append(tmp[0])
            if len_num == 1 and len(tmp) > 1 and num[0] == tmp[0]:
                    tmpdict = {}
                    tmpdict["type"] = "group"
                    tmpdict["info"] = tmp[1]
                    tree.append(tmpdict)
            if len_num == 1 and len(tmp) == 1 and num[0] == tmp[0]:
                (code, resultMSG) = commands.getstatusoutput('rpm -qg "' + tmp[0] + '"')
                if tmp[0] in resultMSG:
                    tree = []
                    tmpdict = {}
                    tmpdict["type"] = "error"
                    tmpdict["info"] = resultMSG
                    tree.append(tmpdict)
                    return Response(tree, status=status.HTTP_200_OK)
                if code != 0:
                    return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                name = resultMSG.split('\n')
                for i in range(len(name)):
                    tmpdict = {}
                    tmpdict["type"] = "pac"
                    tmpdict["info"] = name[i].strip()
                    tree.append(tmpdict)
                return Response(tree, status=status.HTTP_200_OK)
            if len_num == 2 and len(tmp) == 2 and num[0] == tmp[0] and num[1] == tmp[1]:
                (code, resultMSG) = commands.getstatusoutput('rpm -qg "' + tmp[0] + '/' + tmp[1] + '"')
                if tmp[0] in resultMSG:
                    tree = []
                    tmpdict = {}
                    tmpdict["type"] = "error"
                    tmpdict["info"] = resultMSG
                    tree.append(tmpdict)
                    return Response(tree, status=status.HTTP_200_OK)
                if code != 0:
                    return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                name = resultMSG.split('\n')
                for i in range(len(name)):
                    tmpdict = {}
                    tmpdict["type"] = "pac"
                    tmpdict["info"] = name[i].strip()
                    tree.append(tmpdict)
                return Response(tree, status=status.HTTP_200_OK)
        return Response(tree, status=status.HTTP_200_OK)


def getRpm():
    version = ''
    tmp = os.popen('rpm --version').readline()
    pattern = re.compile('\d+(\.\d+)*')
    target = pattern.search(tmp)
    if target is not None:
        version = target.group()
    return version.strip()
