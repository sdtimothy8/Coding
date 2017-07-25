#!/usr/bin/python
# coding=utf-8
from configobjftp import ConfigObj
import commands


class IP_Operate():

    def __init__(self):
        pass

    def check_ip(self, ipaddr):
        """
        Check the IP address is in accordance with the specification
        """
        addr = ipaddr.strip().split('.')
        error = "Invalid IP address."
        if len(addr) > 4:
            return 1, error
        for i in range(len(addr)):
            try:
                addr[i] = int(addr[i])
            except:
                return 2, error
            if addr[i] <= 255 and addr[i] >= 0:
                pass
            else:
                print addr[i]
                return 3, error
        return 0, ""

    def check_mask(self, mask_str):
        """
        Check whether the mask is conform to the specifications
        """
        addr = mask_str.strip().split('.')
        error = "Invalid netmask."
        if len(addr) != 4:
            return 1, error
        for i in range(len(addr)):
            try:
                addr[i] = int(addr[i])
            except:
                return 2, error
        if addr[0] <= 0:
            return 3, error
        for mask in addr:
            masktemp = bin(mask).split('0b')
            if masktemp[0] is '-':
                return 4, error
            masknum = masktemp[1]
            if len(masknum) > 8:
                return 5, error
            else:
                zeronum = '0' * (8 - len(masknum))
                masknum = zeronum + masknum
            if '01' in masknum:
                return 6, error
        return 0, ""

    def add_ip(self, ipaddr, mask=None):
        """
        Add an IP address in the configuration file
        """
        # data = {'ip':"","mask":""}
        result = {"type": "", "message": ""}
        if not ipaddr:
            result['type'] = 1
            result['message'] = "The new IP address is empty."
            return result['type'], result['message']
        code, result_MSG = self.check_ip(ipaddr)
        if code != 0:
            result['type'] = 2
            result['message'] = result_MSG
            return result['type'], result['message']
        if mask:
            code, result_MSG = self.check_mask(mask)
            if code != 0:
                result['type'] = 3
                result['message'] = "Invalid netmask."
                return result['type'], result['message']
            else:
                cmd = "cat /etc/hosts.deny |grep \"^vsftpd:"+ipaddr+"/"+mask+"$\""
                (code, result_MSG) = commands.getstatusoutput(cmd)
                if code == 0:
                    result['type'] = 4
                    result['message'] = "The new IP address already exist."
                    return result['type'], result['message']
                cmd = "echo \"vsftpd:"+ipaddr+"/"+mask+"\" >>/etc/hosts.deny"
                (code, result_MSG) = commands.getstatusoutput(cmd)
                if code != 0:
                    result['type'] = 5
                    result['message'] = result_MSG
                    return result['type'], result['message']
        else:
            cmd = "cat /etc/hosts.deny |grep \"^vsftpd:"+ipaddr+"$\""
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code == 0:
                result['type'] = 6
                result['message'] = "The new IP address already exist."
                return result['type'], result['message']
            cmd = "echo \"vsftpd:"+ipaddr+"\" >>/etc/hosts.deny"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 7
                result['message'] = result_MSG
                return result['type'], result['message']
        result['type'] = 0
        result['message'] = ""
        return result['type'], result['message']

    def delete_ip(self, ipaddr, mask=None):
        """
        In the configuration file to delete an IP address
        """
        # data = {'ip':"","mask":""}
        result = {"type": 0, "message": ""}
        if not ipaddr:
            result['type'] = 1
            result['message'] = "The Data item is empty."
            return result['type'], result['message']
        if mask:
            cmd = "sed -i \"/^vsftpd:"+ipaddr+"\/"+mask+"$/d\" /etc/hosts.deny"
            (code, result_MSG) = commands.getstatusoutput(cmd)
            if code != 0:
                result['type'] = 2
                result['message'] = result_MSG
                return result['type'], result['message']
            result['type'] = 0
            result['message'] = ""
            return result['type'], result['message']
        cmd = "sed -i \"/^vsftpd:"+ipaddr+"$/d\" /etc/hosts.deny"
        (code, result_MSG) = commands.getstatusoutput(cmd)
        if code != 0:
            result['type'] = 3
            result['message'] = result_MSG
            return result['type'], result['message']
        result['type'] = 0
        result['message'] = ""
        return result['type'], result['message']
