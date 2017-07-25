#!/usr/bin/python
# coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from configobjftp import ConfigObj
import os
import sys
import re
import commands
from ftp.check_file import Check_File_Exists as CheckFile
from ftp.reset_config import Reset_Default_Config as ResetConfig
from ftp.ip_operate import IP_Operate


class VsftpdStatus(APIView):

    def get(self, request):
        """
        Query the state of the FTP.
        """
        ftp_status = {"status": -1, "message": ""}
        cmd = "service vsftpd status |grep running"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code == 0:
            ftp_status['status'] = 1
        else:
            ftp_status['status'] = 0
            ftp_status['message'] = result_MSG
        return Response(ftp_status, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Modify the state of the FTP.
        """
        current_state = request.data
        cmd = 'service vsftpd '
        if int(current_state['status']):
            cmd = cmd + 'stop'
            (code, modify_result) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(modify_result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            cmd = cmd + 'start'
            (code, modify_result) = commands.getstatusoutput(cmd)
            if code != 0:
                return Response(modify_result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("success", status=status.HTTP_200_OK)


class VsftpdLinks(APIView):
    """
    get ftplinks information
    """
    def get(self, request):
        links = []
        (code, links_info) = commands.getstatusoutput('netstat -napt |grep vsftpd')
        if code == 0:
            data = links_info.split('\n')
            for i in range(len(data)):
                tmp = data[i].strip().split()
                tmpdict = {}
                if len(tmp) == 7:
                    tmpdict['local_add'] = tmp[3]
                    tmpdict['remote_add'] = tmp[4]
                    tmpdict['state'] = tmp[5]
                    tmpdict['pid'] = tmp[6]
                    links.append(tmpdict)
        return Response(links, status=status.HTTP_200_OK)

User_Config_INIT = {
    # "具有读写的权限"
    # "local_root":"",
    "virtual_use_local_privs": "YES",
    "write_enable": "YES",
    "anon_world_readable_only": "NO",
    "anon_upload_enable": "NO",
    "anon_mkdir_write_enable": "NO",
    "anon_other_write_enable": "NO",
    "idle_session_timeout": 120,
    "data_connection_timeout": 120,
    "max_clients": 0,
    "max_per_ip": 0,
    "guest_enable": "YES"  # 允许访问
    }

User_Config_Items = [
    "local_root",  # readonly
    "virtual_use_local_privs",
    "write_enable",
    "anon_world_readable_only",
    "anon_upload_enable",
    "anon_mkdir_write_enable",
    "anon_other_write_enable",
    "idle_session_timeout",
    "data_connection_timeout",
    "max_clients",
    "max_per_ip",
    "guest_enable"
    ]


class User(APIView):

    def get(self, request):
        userlist = []
        i = 0
        if not os.path.exists("/etc/vsftpd/vsftpd_user"):
            (code, resultTouch) = commands.getstatusoutput('touch /etc/vsftpd/vsftpd_user')
            return Response(userlist, status=status.HTTP_200_OK)
        fileobj = open('/etc/vsftpd/vsftpd_user')
        for data in fileobj:
            tmpdict = {}
            i = i + 1
            if i % 2:
                name = data.strip().split('\n')
                tmpdict['name'] = name[0]
                cmd = "cp  /etc/vsftpd/vsftpd_login/" + tmpdict['name'] + " /etc/vsftpd/vsftpd_login/" + tmpdict['name'] + ".conf"
                (code, result_MSG) = commands.getstatusoutput(cmd)
                if code != 0:
                    tmpdict['result'] = 1
                    tmpdict['message'] = result_MSG
                    userlist.append(tmpdict)
                    continue
                config_file = '/etc/vsftpd/vsftpd_login/' + tmpdict['name'] + ".conf"
                try:
                    config = ConfigObj(config_file)
                except:
                    tmpdict['result'] = 2
                    tmpdict['message'] = "Can't find the configuration file"
                    userlist.append(tmpdict)
                    continue
                key = config.keys()
                if 'local_root' in key:
                    tmpdict['homedir'] = config['local_root']
                else:
                    tmpdict['homedir'] = "Unknown"
                tmpdict['result'] = 0
                userlist.append(tmpdict)
                cmd = "rm -rf /etc/vsftpd/vsftpd_login/"+tmpdict['name']+".conf"
                commands.getstatusoutput(cmd)
        fileobj.close()
        return Response(userlist, status=status.HTTP_200_OK)

    def post(self, request):
        """
        add a user
        """
        # userinfo = {"name":"","config":{},"passwd":"","homedir":""}
        userinfo = request.data
        result = {"type": 0, "message": ""}
        check = CheckFile()
        if not userinfo:
            result['type'] = 1
            result['message'] = "The user information cannot be empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('name' not in userinfo) or ('passwd' not in userinfo) or ('homedir' not in userinfo):
            result['type'] = 2
            result['message'] = "Add a user must specify a user name,passwd,shared directories and configuration items."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        (code, result_MSG) = check.check_file()
        if code != 0:
            result['type'] = 3
            result['message'] = result_MSG
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "cat /etc/vsftpd/vsftpd_user |grep \"^" + userinfo['name'] + "$\""
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code == 0:
            result['type'] = 4
            result['message'] = "User name already exists."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not re.match('/var/ftp', userinfo['homedir']):
            result['type'] = 5
            result['message'] = "Shared directory must be under /var/ftp."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not os.path.exists(userinfo['homedir']):
            cmd = "mkdir  -p " + userinfo['homedir']
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 7
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            cmd = "chmod " + "700 " + userinfo['homedir']
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 9
                result['message'] = result_MSG
                cmd = "rm -rf " + userinfo['homedir']
                commands.getstatusoutput(cmd)
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            cmd = "chown -R ftp:ftp " + userinfo['homedir']
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 11
                result['message'] = result_MSG
                cmd = "rm -rf " + userinfo['homedir']
                commands.getstatusoutput(cmd)
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        config_file = "/etc/vsftpd/vsftpd_login/" + userinfo['name']
        cmd = "rm -rf " + config_file
        commands.getstatusoutput(cmd)
        config = ConfigObj()
        config.filename = config_file
        config['local_root'] = userinfo['homedir']
        # for i in User_Config_INIT:
        #    config[i] = User_Config_INIT[i]
        # config.write()
        cmd = "cp -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_user.bak"
        cmd_1 = "echo " + userinfo['name'] + " >> /etc/vsftpd/vsftpd_user ; echo " + userinfo['passwd'] + " >> /etc/vsftpd/vsftpd_user"
        cmd_2 = "mv -f /etc/vsftpd/vsftpd_login.db /etc/vsftpd/vsftpd_login.db.bak"
        cmd_3 = "db_load -T -t hash -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_login.db"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        (code_1, result_MSG_1) = commands.getstatusoutput(cmd_1)
        (code_2, result_MSG_2) = commands.getstatusoutput(cmd_2)
        (code_3, result_MSG_3) = commands.getstatusoutput(cmd_3)
        if (code != 0) or (code_1 != 0) or (code_2 != 0) or (code_3 != 0):
            result['type'] = 12
            result['message'] = "Not support the user name or password."
            cmd = "mv -f /etc/vsftpd/vdftpd_user.bak  /etc/vsftpd/vsftpd_user; mv -f /etc/vsftpd/vsftpd_login.db.bak /etc/vsftpd/vsftpd_login.db"
            commands.getstatusoutput(cmd)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # if userconfig.has_key('config'):
        boolitems = []
        valueitems = []
        for i in range(1, 7):
            boolitems.append(User_Config_Items[i])
        for i in range(7, 11):
            valueitems.append(User_Config_Items[i])
        for i in userinfo:
            if i in boolitems:
                if (userinfo[i] == "YES") or (userinfo[i] == "NO"):
                    config[i] = userinfo[i]
            else:
                if i in valueitems:
                    config[i] = userinfo[i]
        config['guest_enable'] = "YES"
        config.write()
        result['type'] = 0
        cmd = "rm -rf /etc/vsftpd/vdftpd_user.bak; rm -rf /etc/vsftpd/vsftpd_login.db.bak "
        commands.getstatusoutput(cmd)
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        delete a user
        """
        # userinfo = {"name":""}
        userinfo = request.data
        result = {"type": 0, "message": ""}
        check = CheckFile()
        if not userinfo:
            result['type'] = 1
            result['message'] = "The user information cannot be empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('name' not in userinfo):
            result['type'] = 2
            result['message'] = "Must specify a user name."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        code, result_MSG = check.check_file()
        if code != 0:
            result['type'] = 3
            result['message'] = result_MSG
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "cat /etc/vsftpd/vsftpd_user |grep \"^" + userinfo['name'] + "$\""
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 4
            result['message'] = "User name does not exist."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "cp -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_user.bak;mv -f /etc/vsftpd/vsftpd_login.db /etc/vsftpd/vsftpd_login.db.bak"
        commands.getstatusoutput(cmd)
        cmd = "sed -i \"/^" + userinfo['name'] + "$/{n;d}\" /etc/vsftpd/vsftpd_user;sed -i \"/^" + userinfo['name'] + "$/d\" /etc/vsftpd/vsftpd_user"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 6
            result['message'] = result_MSG
            cmd = "mv -f /etc/vsftpd/vdftpd_user.bak  /etc/vsftpd/vsftpd_user; mv -f /etc/vsftpd/vsftpd_login.db.bak /etc/vsftpd/vsftpd_login.db"
            commands.getstatusoutput(cmd)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "db_load -T -t hash -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_login.db"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 7
            result['message'] = result_MSG
            cmd = "mv -f /etc/vsftpd/vdftpd_user.bak  /etc/vsftpd/vsftpd_user; mv -f /etc/vsftpd/vsftpd_login.db.bak /etc/vsftpd/vsftpd_login.db"
            commands.getstatusoutput(cmd)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "rm -rf /etc/vsftpd/vsftpd_login/" + userinfo['name'] + "; rm -rf /etc/vsftpd/vsftpd_user.bak;rm -rf /etc/vsftpd/vsftpd_login.db.bak"
        commands.getstatusoutput(cmd)
        result['type'] = 0
        return Response(result, status=status.HTTP_200_OK)


class UserInfo(APIView):

    def get(self, request, username):
        """
        Query the user's configuration information
        """
        # username = request.data.get('name')
        # userinfo = request.data
        userconfig = {"config": {}, "result": {}}
        result = {"type": 0, "message": ""}
        check = CheckFile()
        if (not username):
            result['type'] = 1
            result['message'] = "Invalid user name parameter."
            result['name'] = username
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # username = userinfo['name']
        code, result_MSG = check.check_file()
        if code != 0:
            result['type'] = 2
            result['message'] = result_MSG
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "cp /etc/vsftpd/vsftpd_login/" + username + "  /etc/vsftpd/vsftpd_login/" + username + ".conf"
        commands.getstatusoutput(cmd)
        config_file = '/etc/vsftpd/vsftpd_login/' + username + ".conf"
        try:
            config = ConfigObj(config_file)
        except:
            result['type'] = 3
            result['message'] = "Can't find the corresponding configuration file."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        key = config.keys()
        if 'local_root' in key:
            userconfig['homedir'] = config['local_root']
        else:
            userconfig['homedir'] = "Unknown"
        for i in range(1, len(User_Config_Items)-1):
            if User_Config_Items[i] in key:
                userconfig['config'][User_Config_Items[i]] = config[User_Config_Items[i]]
            else:
                userconfig['config'][User_Config_Items[i]] = User_Config_INIT[User_Config_Items[i]]
        userconfig['result']['type'] = 0
        userconfig['result']['message'] = ""
        cmd = "rm -rf  /etc/vsftpd/vsftpd_login/" + username + ".conf"
        commands.getstatusoutput(cmd)
        return Response(userconfig, status=status.HTTP_200_OK)


class UserConfig(APIView):

    def put(self, request):
        """
        Modify the user configuration information
        """
        # userconfig = {"name":"","config":{},"new_passwd":""}
        result = {"type": 0, "message": ""}
        userconfig = request.data
        username = request.data.get('name')
        check = CheckFile()
        if (not username) and (not userconfig):
            result['type'] = 1
            result['message'] = "Invalid parameter."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        code, result_MSG = check.check_file()
        if code != 0:
            result['type'] = 2
            result['message'] = result_MSG
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "cp /etc/vsftpd/vsftpd_login/" + username + "  /etc/vsftpd/vsftpd_login/" + username + ".conf"
        commands.getstatusoutput(cmd)
        config_file = '/etc/vsftpd/vsftpd_login/' + username + ".conf"
        try:
            config = ConfigObj(config_file)
        except:
            result['type'] = 3
            result['message'] = "Can't find the corresponding configuration file."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        key = config.keys()
        if 'new_passwd' in userconfig:
            cmd = "rm -rf /etc/vsftpd/vsftpd_user.bak;rm -rf /etc/vsftpd/vsftpd_login.db.bak"
            commands.getstatusoutput(cmd)
            cmd = "cp /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_user.bak; cp /etc/vsftpd/vsftpd_login.db /etc/vsftpd/vsftpd_login.db.bak"
            commands.getstatusoutput(cmd)
            cmd = "sed -i \"/^" + username + "$/{n;d}\" /etc/vsftpd/vsftpd_user"
            cmd_1 = "sed -i \"/^" + username + "$/a\\" + userconfig['new_passwd'] + "\" /etc/vsftpd/vsftpd_user"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            (code_1, result_MSG_1) = commands.getstatusoutput(cmd_1)
            if (code != 0) or (code_1 != 0):
                result['type'] = 7
                result['message'] = "Update password failure."
                cmd = "mv -f /etc/vsftpd/vdftpd_user.bak  /etc/vsftpd/vsftpd_user; mv -f /etc/vsftpd/vsftpd_login.db.bak /etc/vsftpd/vsftpd_login.db"
                commands.getstatusoutput(cmd)
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            cmd = "db_load -T -t hash -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_login.db"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 8
                result['message'] = result_MSG
                cmd = "mv -f /etc/vsftpd/vdftpd_user.bak  /etc/vsftpd/vsftpd_user; mv -f /etc/vsftpd/vsftpd_login.db.bak /etc/vsftpd/vsftpd_login.db"
                commands.getstatusoutput(cmd)
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            cmd = "rm -rf /etc/vsftpd/vsftpd_user.bak;rm -rf /etc/vsftpd/vsftpd_login.db.bak"
            commands.getstatusoutput(cmd)
        boolitems = []
        valueitems = []
        for i in range(1, 7):
            boolitems.append(User_Config_Items[i])
        for i in range(7, 11):
            valueitems.append(User_Config_Items[i])
        for i in userconfig:
            if i in boolitems:
                if (userconfig[i] == "YES") or (userconfig[i] == "NO"):
                    config[i] = userconfig[i]
            else:
                if i in valueitems:
                    config[i] = userconfig[i]
        config.write()
        result['type'] = 0
        result['message'] = ""
        cmd = "mv -f  /etc/vsftpd/vsftpd_login/" + username + ".conf  /etc/vsftpd/vsftpd_login/" + username
        commands.getstatusoutput(cmd)
        return Response(result, status=status.HTTP_200_OK)

FTP_Config_Items = [
    "listen",
    "guest_enable",
    "guest_username",
    "virtual_use_local_privs",
    "tcp_wrappers",
    "pam_service_name",
    "chroot_list_enable",
    "allow_writeable_chroot",
    "chroot_local_user",
    "local_enable",

    "write_enable",
    "pasv_enable",
    "anonymous_enable",
    "anon_world_readable_only",
    "anon_other_write_enable",
    "anon_mkdir_write_enable",
    "anon_upload_enable",
    "no_anon_password"
    ]

FTP_Config_INIT = {
    "listen": "YES",
    "listen_ipv6": "NO",
    "guest_enable": "YES",
    "guest_username": "ftp",
    "virtual_use_local_privs": "YES",
    "tcp_wrappers": "YES",
    "pam_service_name": "vsftpd",
    "chroot_list_enable": "NO",
    "allow_writeable_chroot": "YES",
    "user_config_dir": "/etc/vsftpd/vsftpd_login",
    "local_enable": "YES",

    "write_enable": "NO",
    "pasv_enable": "YES",
    "chroot_local_user": "YES",
    "anonymous_enable": "NO",
    "anon_world_readable_only": "NO",
    "anon_other_write_enable": "NO",
    "anon_mkdir_write_enable": "NO",
    "anon_upload_enable": "NO",
    "no_anon_password": "NO",
    }


class FTPConfig(APIView):

    def get(self, request):
        """
        Query the FTP server configuration
        """
        ftpconfig = {"readonly_config": {}, "config": {}, "result": {}}
        config_file = '/etc/vsftpd/vsftpd.conf'
        try:
            config = ConfigObj(config_file)
        except:
            ftpconfig['result']['type'] = 1
            ftpconfig['result']['message'] = "Can't find vsftpd.conf"
            return Response(ftpconfig, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        key = config.keys()
        for i in range(0, 10):
            if FTP_Config_Items[i] in key:
                ftpconfig['readonly_config'][FTP_Config_Items[i]] = config[FTP_Config_Items[i]]
            else:
                config[FTP_Config_Items[i]] = FTP_Config_INIT[FTP_Config_Items[i]]
                config.write()
                ftpconfig['readonly_config'][FTP_Config_Items[i]] = FTP_Config_INIT[FTP_Config_Items[i]]
        for i in range(10, len(FTP_Config_Items)):
            if FTP_Config_Items[i] in key:
                ftpconfig['config'][FTP_Config_Items[i]] = config[FTP_Config_Items[i]]
            else:
                ftpconfig['config'][FTP_Config_Items[i]] = FTP_Config_INIT[FTP_Config_Items[i]]
        ftpconfig['result']['type'] = 0
        return Response(ftpconfig, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Modify the FTP server configuration
        """
        result = {"type": 0, "message": ""}
        # ftpconfig = request.data.get('config')
        ftpconfig = request.data
        if not ftpconfig:
            result['type'] = 1
            result['message'] = "Invalid parameter."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "rm -rf /etc/vsftpd/vsftpd.conf.bak"
        commands.getstatusoutput(cmd)
        cmd = "cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.bak"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 2
            result['message'] = "Backup old configuration failed."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        config_file = '/etc/vsftpd/vsftpd.conf'
        try:
            config = ConfigObj(config_file)
        except:
            result['type'] = 3
            result['message'] = "Can't find vsftpd.conf"
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        boolitems = []
        for i in range(10, 18):
            boolitems.append(FTP_Config_Items[i])
        for i in ftpconfig:
            if i in boolitems:
                if (ftpconfig[i] == "YES") or (ftpconfig[i] == "NO"):
                    config[i] = ftpconfig[i]
        config.write()
        cmd = "service vsftpd restart"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 3
            result['message'] = result_MSG
            cmd = "cp /etc/vsftpd/vsftpd.conf.bak /etc/vsftpd/vsftpd.conf ; rm -rf /etc/vsftpd/sftpd.conf.bak ; service vsftpd restart"
            commands.getstatusoutput(cmd)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cmd = "rm -rf /etc/vsftpd/vsftpd.conf.bak"
        commands.getstatusoutput(cmd)
        result['type'] = 0
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Restore the default config.
        """
        reset = ResetConfig()
        result = {"type": 0, "message": ""}
        result['type'], result['message'] = reset.reset_default()
        if result['type'] == 0:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IPLimit(APIView):

    def get(self, request):
        """
        The IP address of the query limit access to FTP
        """
        ip_list = []
        cmd = "cat /etc/hosts.deny|grep vsftpd"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code == 0:
            for line in result_MSG.split('\n'):
                data = line.strip().split(":")
                ip_list.append(data[1])
        return Response(ip_list, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Modify the IP address of the FTP service limit access
        """
        # data = {'old_ip':"","new_ip":"","old_mask":"","new_mask":""}
        ip_data = request.data
        result = {"type": 0, "message": ""}
        IPOperate = IP_Operate()
        if not ip_data:
            result['type'] = 1
            result['message'] = "The data item is empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('old_ip' not in ip_data) or ('new_ip' not in ip_data) or (not ip_data['old_ip']):
            result['type'] = 2
            result['message'] = "IP address empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('new_ip' in ip_data) and ip_data['new_ip']:
            if 'new_mask' in ip_data:
                code, result_MSG = IPOperate.add_ip(ip_data['new_ip'], ip_data['new_mask'])
            else:
                code, result_MSG = IPOperate.add_ip(ip_data['new_ip'])
            if code != 0:
                result['type'] = 3
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if 'old_mask' in ip_data:
                code, result_MSG = IPOperate.delete_ip(ip_data['old_ip'], ip_data['old_mask'])
                if code != 0:
                    if 'new_mask' in ip_data:
                        IPOperate.delete_ip(ip_data['new_ip'], ip_data['new_mask'])
                    else:
                        IPOperate.delete_ip(ip_data['new_ip'])
                    result['type'] = 4
                    result['message'] = result_MSG
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                code, result_MSG = IPOperate.delete_ip(ip_data['old_ip'])
                if code != 0:
                    if 'new_mask' in ip_data:
                        IPOperate.delete_ip(ip_data['new_ip'], ip_data['new_mask'])
                    else:
                        IPOperate.delete_ip(ip_data['new_ip'])
                    result['type'] = 5
                    result['message'] = result_MSG
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if 'old_mask' in ip_data:
                code, result_MSG = IPOperate.delete_ip(ip_data['old_ip'], ip_data['old_mask'])
            else:
                code, result_MSG = IPOperate.delete_ip(ip_data['old_ip'])
            if code != 0:
                result['type'] = 6
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result['type'] = 0
        result['message'] = ""
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Add the IP address of the FTP service limit access
        """
        # data = {'ip':"","mask":""}
        ip_data = request.data
        result = {"type": 0, "message": ""}
        IPOperate = IP_Operate()
        if not ip_data:
            result['type'] = 1
            result['message'] = "The data item is empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('ip' not in ip_data) or (not ip_data['ip']):
            result['type'] = 2
            result['message'] = "IP address empty"
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        code, result_MSG = IPOperate.check_ip(ip_data['ip'])
        if code != 0:
            result['type'] = 3
            result['message'] = result_MSG
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if "mask" in ip_data:
            cmd = "cat /etc/hosts.deny |grep \"^vsftpd:"+ip_data['ip']+"/"+ip_data["mask"]+"$\""
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code == 0:
                result['type'] = 4
                result['message'] = "The IP address already exist."
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            code, result_MSG = IPOperate.check_mask(ip_data['mask'])
            if code != 0:
                result['type'] = 5
                result['message'] = "Netmask is not correct."
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                cmd = "echo \"vsftpd:"+ip_data['ip']+"/"+ip_data['mask']+"\" >>/etc/hosts.deny"
                (code, result_MSG) = commands.getstatusoutput(cmd)
                if code != 0:
                    result['type'] = 6
                    result['message'] = result_MSG
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            cmd = "cat /etc/hosts.deny |grep \"^vsftpd:"+ip_data['ip']+"$\""
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code == 0:
                result['type'] = 7
                result['message'] = "The IP address already exist."
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            cmd = "echo \"vsftpd:"+ip_data['ip']+"\" >>/etc/hosts.deny"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 8
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result['type'] = 0
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Delete the IP address of the FTP service limit access
        """
        # data = {'ip':"","mask":""}
        ip_data = request.data
        result = {"type": 0, "message": ""}
        if not ip_data:
            result['type'] = 1
            result['message'] = "The data item is empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if ('ip' not in ip_data) or (not ip_data['ip']):
            result['type'] = 2
            result['message'] = "IP address empty."
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if 'mask' in ip_data:
            cmd = "sed -i \"/^vsftpd:"+ip_data['ip']+"\/"+ip_data['mask']+"$/d\" /etc/hosts.deny"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 3
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            cmd = "sed -i \"/^vsftpd:"+ip_data['ip']+"$/d\" /etc/hosts.deny"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 4
                result['message'] = result_MSG
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result['type'] = 0
        return Response(result, status=status.HTTP_200_OK)
