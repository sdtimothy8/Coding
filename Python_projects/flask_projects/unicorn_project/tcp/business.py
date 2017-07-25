"""
this module provide classes for TCP Wrapper functions
e.g get info list, add a new rule, delete a rule
"""
from string import strip
from public import functions

__author__ = 'zhuysh@inspur.com'


class TcpBusiness():
    """
    tcp business
    """

    @classmethod
    def getlistinfo(cls, filename):
        """
        read info from sys
        :param filename:
        :return:
        """
        filterfile = functions.launchcmd('grep -v "^#" ' + filename).readlines()
        hostsinfo = []
        for t in filterfile:
            oneinfo = t.split(":", 2)
            if len(oneinfo) == 3:
                hostsinfo.append(oneinfo)
            elif len(oneinfo) == 2:
                oneinfo.append("")
                hostsinfo.append(oneinfo)
            elif len(oneinfo) == 1:
                oneinfo.append("")
                oneinfo.append("")
                hostsinfo.append(oneinfo)

        return hostsinfo

    @classmethod
    def putlistinfo(cls, request, filename):
        """
        write info to sys
        :param request:
        :param filename:
        :return:
        """

        ni_dict = request.data.get("addInfo")
        openconfigfile = open(filename, 'a')
        # openconfigfile = os.open(filename, os.O_APPEND)
        # addInfo = ni_dict
        daemon = ni_dict.get("daemon")
        hosts = ni_dict.get("hosts")
        command = ni_dict.get("command")
        # return Response(daemon+":"+hosts+":"+command,status=status.HTTP_200_OK)
        Writefile = ""
        if "" == command.strip():
            Writefile = str(daemon+":"+hosts+"\n")
        else:
            Writefile = str(daemon+":"+hosts+":"+command+"\n")
        openconfigfile.write(Writefile)
        openconfigfile.close()
        # restr = os.write(openconfigfile, Writefile)
        # os.close(openconfigfile)

        return "success"

    @classmethod
    def deletelistinfo(cls, request, filename):
        """
        delete one tcpwrappers  rules
        :param request:
        :param foramt:
        :return:
        """

        filterfile = functions.launchcmd("cat " + filename).readlines()
        delete_rules = request.data.get("deleteinfo")

        delete_hostsinfo = []

        for daemonline in filterfile:

            # if the flag is true, then wirte this line to the file
            need_write = True
            rule_info = daemonline.replace(":", "").replace(" ", "").replace(",", "")

            # find the lines that need write to the file
            for delete_info in delete_rules:
                delete_info = delete_info.replace(",", "").replace(" ", "").replace(":", "")
                if strip(daemonline).startswith("#"):
                    need_write = True
                elif rule_info == delete_info:
                    need_write = False

            if need_write:
                delete_hostsinfo.append(daemonline)

            # if daemonline.find(delete_daemon) == -1:
            #     delete_hostsinfo.append(daemonline+'\n')

        if len(delete_hostsinfo):
            hosts_file = open(filename, 'w+')
            hosts_file.writelines(delete_hostsinfo)
            hosts_file.close()
        else:
            return 'error'

        return 'success'
