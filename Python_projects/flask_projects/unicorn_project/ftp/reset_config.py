#!/usr/bin/python
# coding=utf-8
from configobjftp import ConfigObj
import os
import commands

FTP_Config_Items = {
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
    "connect_from_port_20": "YES",
    "pasv_enable": "YES",
    "use_localtime": "YES",
    "chroot_local_user": "YES",
    "anonymous_enable": "NO",
    "anon_world_readable_only": "NO",
    "anon_other_write_enable": "NO",
    "anon_mkdir_write_enable": "NO",
    "anon_upload_enable": "NO",
    "no_anon_password": "NO",

    "listen_port": 21
}


class Reset_Default_Config ():

    def __init__(self):
        pass

    def reset_default(self):
        if not os.path.exists("/etc/vsftpd/vsftpd_login"):
            cmd = "mkdir /etc/vsftpd/vsftpd_login"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 1
                result['message'] = result_MSG
                return 1, result_MSG
        else:
            cmd = "rm -rf /etc/vsftpd/vsftpd_login/*"
            commands.getstatusoutput(cmd)
        cmd = "rm -rf /etc/vsftpd/vsftpd_user"
        commands.getstatusoutput(cmd)
        cmd = "rm -rf /etc/vsftpd/vsftpd_login.db"
        commands.getstatusoutput(cmd)
        cmd = "touch /etc/vsftpd/vsftpd_user"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return 2, result_MSG
        cmd = "db_load -T -t hash -f /etc/vsftpd/vsftpd_user /etc/vsftpd/vsftpd_login.db"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return 3, result_MSG
        config = ConfigObj()
        config.filename = "/etc/vsftpd/vsftpd.conf"
        for i in FTP_Config_Items:
            config[i] = FTP_Config_Items[i]
        config.write()
        cmd = "chmod 600 /etc/vsftpd/vsftpd.conf"
        commands.getstatusoutput(cmd)
        cmd = "service vsftpd restart"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            return 4, result_MSG
        cmd = "cat /etc/pam.d/vsftpd |grep vsftpd_login"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code == 0:
            data = result_MSG.split('\n')
            if len(data) == 2:
                if (data[0][0] != '#') and (data[1][0] != '#'):
                    return 0, " "
        cmd = " "
        cmd_1 = " "
        x86_64_file = "/lib64/security/pam_userdb.so"
        x86_file = "/lib/security/pam_userdb.so"
        file_name = ""
        if os.path.exists(x86_64_file):
            file_name = x86_64_file
        else:
            if os.path.exists(x86_file):
                file_name = x86_file
        if file_name != " ":
            cmd = "echo \"#%PAM-1.0\" >/etc/pam.d/vsftpd ; echo \"auth sufficient " + file_name + " db=/etc/vsftpd/vsftpd_login\" >>/etc/pam.d/vsftpd"
            cmd_1 = "echo \"account sufficient " + file_name + " db=/etc/vsftpd/vsftpd_login\" >>/etc/pam.d/vsftpd"
        if (cmd == " ") or (cmd_1 == " "):
            return 5, "pam_userdb.so not exist."
        else:
            (code, result_MSG) = commands.getstatusoutput(cmd)
            (code_1, result_MSG_1) = commands.getstatusoutput(cmd_1)
            if (code != 0) or (code_1 != 0):
                return 6, "/etc/pam.d/vsftpd file error."
        return 0, " "
