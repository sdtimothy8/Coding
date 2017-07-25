#!/usr/bin/env python
# coding=utf8
import time
import os
import sys
import django
import pika
import json
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ksmp.settings'
django.setup()
from apscheduler.scheduler import Scheduler
from agent import utils
from agent import constr
from ksmp import logger
import logging
logging.basicConfig()


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


class HeartBeat(Singleton):

    def __init__(self):
        self.scheduler = Scheduler()
        credentials = pika.PlainCredentials('inspur', 'inspur')
        flag, rabbitmq_ip = utils.getRabbitmqIp()
        # 这里可以连接远程IP，请记得打开远程端口
        parameters = pika.ConnectionParameters(rabbitmq_ip, 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    """
    heartbeat task
    """
    def agentHeartBeat(self):

        logger.debug("agent heart beat begin!")
        self.scheduler.add_interval_job(self.heartBeatWithServer, seconds=3)

        self.scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                if not utils.httpdstate:
                    sys.exit(0)
        except KeyboardInterrupt:
            self.scheduler.shutdown()
        finally:
            self.connection.close()

    def heartBeatWithServer(self):
        agentInfo = {'type': constr.NODE_STATUS, 'token': constr.NODE_TOKEN}
        flag, agentid = utils.getAgentId()
        if not (flag and agentid):
            return
        agentInfo['id'] = agentid
        logger.debug("node hb info : {}".format(str(agentInfo)))
        try:
            self.channel.basic_publish(exchange='exchangeTest', routing_key='heartBeatKey', body=json.dumps(agentInfo))
        except Exception, e:
            logger.error("heartbeat exception: {}".format(e.message))
            credentials = pika.PlainCredentials('inspur', 'inspur')
            flag, rabbitmq_ip = utils.getRabbitmqIp()
            # 这里可以连接远程IP，请记得打开远程端口
            parameters = pika.ConnectionParameters(rabbitmq_ip, 5672, '/', credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            pass
        return True


# if __name__ == '__main__':
#     hb = HeartBeat()
#     hb.agentHeartBeat()
