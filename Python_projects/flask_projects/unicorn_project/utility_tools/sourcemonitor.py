# coding=utf-8
# !/usr/bin/env python
"""
Get the source code analysis summary.
"""
import os
__author__ = 'shaomingwu@inspur.com'

# define the module name.
MOD_LOAD = "load"
MOD_ROUTER = "router"
MOD_TIMES = "times"
MOD_LOG = "log"
MOD_SESSION = "session"
MOD_SYSTEM = "system"
MOD_DNS = "Dns"
MOD_TCP = "tcp"
MOD_TEMPLATES = "templates"
MOD_USERS = "users"
MOD_FIREWALL = "firewall"
MOD_INDEX = "index"
MOD_LOGIN = "login"
MOD_FT = "ft"
MOD_KSMP = "ksmp"
MOD_PRECMD = "precmd"
MOD_RESOURCES = "resources"
MOD_HOST = "host"
MOD_PACKAGES = "packages"
MOD_NETWORK = "network"
MOD_DISKMGR = "diskmgr"
MOD_PUBLIC = "public"
MOD_SYSMONITOR = "sysmonitor"

MOD_DICT = {
    MOD_LOAD: "引导（服务管理）",
    MOD_ROUTER: "路由和网关",
    MOD_TIMES: "系统时间",
    MOD_LOG: "系统日志",
    MOD_SESSION: "会话管理",
    MOD_SYSTEM: "关机",
    MOD_DNS: "DNS设置",
    MOD_TCP: "TCP WRAPPERS",
    MOD_TEMPLATES: "模板",
    MOD_USERS: "用户和群组",
    MOD_FIREWALL: "防火墙",
    MOD_INDEX: "首页",
    MOD_LOGIN: "登录模块",
    MOD_FT: "上传和下载",
    MOD_KSMP: "Unicorn工程配置",
    MOD_PRECMD: "预定命令",
    MOD_RESOURCES: "系统资源监控",
    MOD_HOST: "主机地址",
    MOD_PACKAGES: "软件包展示",
    MOD_NETWORK: "网络接口",
    MOD_DISKMGR: "磁盘管理",
    MOD_PUBLIC: "公共模块",
    MOD_SYSMONITOR: "系统监控",
}

if __name__ == "__main__":
    this_dir = os.path.split(os.path.realpath(__file__))[0]
    resultfile = "%s/source_monitor.log" % this_dir
    # print(resultfile)

    top_dir = os.path.dirname(this_dir)

    file_line_num = 0
    dir_line_num = 0
    all_num = 0
    mod_index = 0

    with open(resultfile, 'w') as outputfile:
        outputfile.write("Start analysis the source code.\n")
        for root, dirs, files in os.walk(top_dir):
            for onedir in dirs:
                if onedir.startswith('.'):
                    print("ignore the dir of %s \n" % onedir)
                    continue
                # process the sub-directory.
                subdirectory = "%s/%s" % (top_dir, onedir)
                dir_line_num = 0

                for subroot, subdirs, subfiles in os.walk(subdirectory):
                    for filename in subfiles:
                        file_line_num = 0
                        if filename in ('manage.py', 'py_coderule_check.py', 'pep8_unicorn.py'):
                            pass
                        elif filename.endswith(".py"):
                            fullpath = os.path.join(subroot, filename)
                            # if filename == "tests.py":
                            # outputfile.write("    Source file: %s " % fullpath)

                            with open(fullpath) as onefile:
                                for oneline in onefile:
                                    file_line_num += 1
                                    dir_line_num += 1
                                    all_num += 1

                            # if filename == "tests.py":
                            # outputfile.write(" : %d \n" % file_line_num)
                if dir_line_num == 0:
                    continue

                mod_index += 1
                outputfile.write("%d\t %-30s %d \n" % (mod_index, MOD_DICT.get(onedir, onedir), dir_line_num))

            break
        outputfile.write("The total number of unicorn project is [%d]\n" % all_num)
