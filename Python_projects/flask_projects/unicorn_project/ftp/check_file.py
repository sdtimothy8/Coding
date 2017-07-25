#!/usr/bin/python
# coding=utf-8
from configobjftp import ConfigObj
import os
import sys
import commands


class Check_File_Exists():

    def __init__(self):
        pass

    def check_file(cls):
        """
        Check the system the necessary configuration file
        """
        file_name = ["/etc/vsftpd/vsftpd.conf", "/etc/vsftpd/vsftpd_user", "/etc/vsftpd/vsftpd_login.db", "/etc/pam.d/vsftpd", "/etc/vsftpd/vsftpd_login"]
        for i in range(len(file_name)):
            if not os.path.exists(file_name[i]):
                return 1, "The file is missing,please restore the default settings."
        cmd = "cat /etc/pam.d/vsftpd |grep vsftpd_login"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code == 0:
            data = result_MSG.split('\n')
            if len(data) == 2:
                if (data[0][0] != '#') and (data[1][0] != '#'):
                    return 0, ""
        cmd = " "
        cmd_1 = " "
        x86_64_file = "/lib64/security/pam_userdb.so"
        x86_file = "/lib/security/pam_userdb.so"
        file_name = " "
        if os.path.exists(x86_64_file):
            file_name = x86_64_file
        else:
            if os.path.exists(x86_file):
                file_name = x86_file
        if file_name != " ":
            cmd = "echo \"#%PAM-1.0\" >/etc/pam.d/vsftpd ; echo \"auth sufficient " + file_name + " db=/etc/vsftpd/vsftpd_login\" >>/etc/pam.d/vsftpd"
            cmd_1 = "echo \"account sufficient " + file_name + " db=/etc/vsftpd/vsftpd_login\" >>/etc/pam.d/vsftpd"
        if (cmd == " ") or (cmd_1 == " "):
            return 2, "pam_userdb.so not exist. "
        else:
            (code, result_MSG) = commands.getstatusoutput(cmd)
            (code_1, result_MSG_1) = commands.getstatusoutput(cmd_1)
            if (code != 0) or (code_1 != 0):
                return 3, "/etc/pam.d/vsftpd file error."
            else:
                return 0, ""
