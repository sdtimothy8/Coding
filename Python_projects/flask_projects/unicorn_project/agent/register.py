#!/usr/bin/env python
# coding=utf8
import json
import commands
import time
import os
import sys
import django
import fcntl
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ksmp.settings'
django.setup()
from agent import utils
from ksmp import logger
from agent import constr
from agent import heartBeat

__author__ = 'zhuysh@inspur.com'


class Singleton(object):
    """
    Singleton class
    """
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Register(Singleton):
    def __init__(self):
        self.flag, self.server_info = utils.read_settings()

    def register_agent(self):

        if self.flag:
            api = "{}".format('/server/api/register/')
            # api = "{}".format('/api/resources/')  # for test
            nodeinfo = {constr.ID: str(self.server_info["AGENTID"]),
                        constr.ALIAS: self.server_info["ALIAS"],
                        constr.PORT: 8000,
                        constr.TOKEN: constr.NODE_TOKEN,
                        constr.STATUS: constr.RUNNING}
            params = json.dumps(nodeinfo)

            obj = utils.postinfo(20, api, self.server_info["IP"], self.server_info["PORT"], params, method='POST')

            if str(obj) == '200' or str(obj) == '204':
                logger.debug("register_agent SUCESS!")
                hb = heartBeat.HeartBeat()
                hb.agentHeartBeat()
                return True
            else:
                logger.debug("register_agent failed! ==> {}".format(str(obj)))
                time.sleep(20)
                self.register_agent()

        else:
            logger.error("agent register fialed! : ".format(str(self.server_info)))

        return False


if __name__ == '__main__':
    try:
        pid_path = sys.path[0] + '/agent.pid'
        with open(pid_path, 'r+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            data = f.read()
            print data
            if int(data) == 0:
                f.write(str(os.getpid()))
            else:
                sys.exit(0)
    except:
        sys.exit(0)
    rg = Register()
    rg.register_agent()
