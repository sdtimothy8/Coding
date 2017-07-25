from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import commands
import os


class user(APIView):
    """
    get user lists
    """
    def get(self, request):
        fileobj = open('/etc/group')
        grouplist = {"groups": []}

        for line in fileobj:
            tmp = line.split(':')
            tmpdict = {}
            tmpdict['gname'] = tmp[0]
            tmpdict['gid'] = tmp[2]
            tmpdict['gusers'] = tmp[3].replace('\n', '')
            grouplist['groups'].append(tmpdict)

        fileobj = open('/etc/passwd')
        userlist = {"users": []}

        for line in fileobj:
            tmp = line.split(':')
            tmpdict = {}
            tmpdict['username'] = tmp[0]
            tmpdict['uid'] = tmp[2]
            tmpdict['gid'] = tmp[3]
            flag_no_group_by_gid = 1
            for groupdict in grouplist['groups']:
                if groupdict['gid'] == tmp[3]:
                    tmpdict['gname'] = groupdict['gname']
                    flag_no_group_by_gid = 0
            if flag_no_group_by_gid == 1:
                tmpdict['gname'] = " "
            tmpdict['fullname'] = tmp[4]
            tmpdict['homedir'] = tmp[5]
            tmpdict['shelldir'] = tmp[6].replace('\n', '')
            userlist['users'].append(tmpdict)

        return Response(userlist, status=status.HTTP_200_OK)

    def post(self, request):
        """
        add a new user
        """
        userinfo = request.data
        fileobj = open('/etc/passwd')
        for line in fileobj:
            tmp = line.split(':')
            if tmp[0] == userinfo['uname']:  # user has exist
                return Response("user has exist, please change a new name!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fileobj = open('/etc/group')
        for line in fileobj:
            tmp = line.split(':')
            if tmp[0] == userinfo['uname']:  # user has exist
                return Response("group has exist, please change a new user name!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cmd = 'useradd '

        if 'uname' in userinfo:
            cmd = cmd + userinfo['uname']

        if 'fullname' in userinfo:
            cmd = cmd + ' -c ' + userinfo['fullname'].replace(' ', '\ ')  # if fullname has blank

        if 'password' in userinfo:
            cmd = cmd + ' -p ' + userinfo['password']

        if 'shell' in userinfo:
            cmd = cmd + ' -s ' + userinfo['shell']

        if 'uid' in userinfo:
            if userinfo['uid'] != '':  # the user id is setted by user
                cmd = cmd + ' -u ' + userinfo['uid']

        if 'gid' in userinfo:
            if userinfo['gid'] != '':  # the group id is setted by user
                cmd = cmd + ' -g ' + userinfo['gid']

        if 'homedir' in userinfo:
            if userinfo['homedir'] != '':  # the home dir is setted by user
                if os.path.exists(userinfo['homedir']) == True:
                    return Response("home dir has exist, please make a new dir!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                cmd = cmd + ' -d ' + userinfo['homedir']
        if userinfo['homedir'] == '':
            strdir = '/home/' + userinfo['uname']
            if os.path.exists(strdir) == True:
                return Response("home dir has exist, please make a new dir!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        (code, resultMSG) = commands.getstatusoutput(cmd)

        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'password' in userinfo:
            cmd = "echo \'" + userinfo['uname'] + ":" + userinfo['password'] + "\'| chpasswd"
            (codePasswd, resultPasswd) = commands.getstatusoutput(cmd)
            if codePasswd != 0:
                return Response(resultPasswd, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        edit user info
        """
        userinfo = request.data

        if ('newname' in userinfo) & ('uname' in userinfo):
            if (userinfo['newname'] != '') & (userinfo['newname'] != userinfo['uname']):  # user changed the username
                cmd = 'usermod -l ' + userinfo['newname'] + ' ' + userinfo['uname']  # update the username
                (code, resname) = commands.getstatusoutput(cmd)
                if code != 0:
                    return Response(resname, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'fullname' in userinfo:
            cmd = 'usermod -c ' + userinfo['fullname'].replace(' ', '\ ') + ' ' + userinfo['newname']
            (code, resfullname) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(resfullname, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'password' in userinfo:
            if userinfo['password'] != '':
                cmd = "echo \'" + userinfo['password'] + "\' | passwd --stdin " + userinfo['newname']
                (code, respasswd) = commands.getstatusoutput(cmd)
                if code != 0:
                    return Response(respasswd, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'shell' in userinfo:
            cmd = 'usermod -s ' + userinfo['shell'] + ' ' + userinfo['newname']
            (code, resshell) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(resshell, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        """
        delete user(s)
        """
        userlist = request.data

        for user in userlist['users']:
            if 'uname' in user:
                cmd = 'userdel -r ' + user['uname']
                (code, result) = commands.getstatusoutput(cmd)
                if code != 0:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_200_OK)


class userdetail(APIView):
    """
    get user information by username
    """
    def get(self, request, username):
        fileobj = open('/etc/passwd')
        userlist = {"users": []}

        for line in fileobj:
            tmp = line.split(':')
            if tmp[0] == username:
                tmpdict = {}
                tmpdict['username'] = tmp[0]
                tmpdict['uid'] = tmp[2]
                tmpdict['gid'] = tmp[3]
                tmpdict['fullname'] = tmp[4]
                tmpdict['homedir'] = tmp[5]
                tmpdict['shelldir'] = tmp[6].replace('\n', '')
                userlist['users'].append(tmpdict)

        return Response(userlist, status=status.HTTP_200_OK)


class group(APIView):
    """
    get groups list
    """
    def get(self, request):
        fileobj = open('/etc/group')
        grouplist = {"groups": []}

        for line in fileobj:
            tmp = line.split(':')
            tmpdict = {}
            tmpdict['gname'] = tmp[0]
            tmpdict['gid'] = tmp[2]
            tmpdict['gusers'] = tmp[3].replace('\n', '')
            grouplist['groups'].append(tmpdict)

        return Response(grouplist, status=status.HTTP_200_OK)

    def post(self, request):
        """
        add a group
        """
        groupinfo = request.data
        cmd = 'groupadd '
        # add a new group
        if 'gname' in groupinfo:
            cmd = cmd + groupinfo['gname']

        if 'gid' in groupinfo:
            if groupinfo['gid'] != '':  # the group id is setted by user
                cmd = cmd + ' -g ' + groupinfo['gid']

        (code, resultMSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return Response(resultMSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        delete group(s)
        """
        grouplist = request.data

        for group in grouplist['groups']:
            if 'gname' in group:
                cmd = 'groupdel ' + group['gname']
                (code, result) = commands.getstatusoutput(cmd)
                if code != 0:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_200_OK)

    def put(self, request):
        """
        change user(s) in group
        """
        grouplist = request.data
        type = grouplist['type']

        # add user into group
        if type == 'add':
            operation = ' -a '
        elif type == 'delete':
            operation = ' -d '
        else:
            return Response('arg error', status=status.HTTP_400_BAD_REQUEST)

        for group in grouplist['groups']:
            if 'gname' in group:
                cmd = 'gpasswd' + operation + group['uname'] + ' ' + group['gname']
                (code, result) = commands.getstatusoutput(cmd)
                if code != 0:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('success', status=status.HTTP_202_ACCEPTED)


class groupdetail(APIView):
    """
    get group users by group name
    """
    def get(self, request, gname):
        fileobj = open('/etc/group')
        grouplist = {"groups": []}

        for line in fileobj:
            tmp = line.split(':')
            if tmp[0] == gname:
                tmpdict = {}
                tmpdict['gname'] = tmp[0]
                tmpdict['gusers'] = tmp[3].replace('\n', '')
                grouplist['groups'].append(tmpdict)

        return Response(grouplist, status=status.HTTP_200_OK)
