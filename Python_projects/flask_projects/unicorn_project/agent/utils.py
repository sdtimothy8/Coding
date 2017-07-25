#!/usr/bin/env python
# coding=utf8
import uuid
import sys
import httplib
import json
import commands
from string import strip
from ksmp import settings
from ksmp import logger


def read_settings():
    """
    get server info (IP and port)
    :return:
    """

    server_settings_path = "{}{}".format(settings.BASE_DIR, '/uniserver.ini')
    agent_settings_path = "{}{}".format(settings.BASE_DIR, '/uniagent.ini')
    server = {}
    try:
        with open(server_settings_path) as settingsInfo:
            lines = settingsInfo.readlines()
            for line in lines:
                if strip(line).startswith("server_ip="):
                    server['IP'] = strip(line.split('server_ip=')[1])
                elif strip(line).startswith("server_port="):
                    server['PORT'] = strip(line.split('server_port=')[1])
                elif strip(line).startswith("node_name="):
                    server['ALIAS'] = strip(line.split('node_name=')[1])
        with open(agent_settings_path) as agentSettings:
            alines = agentSettings.readlines()
            for aline in alines:
                if strip(aline).startswith("agent_id="):
                    server['AGENTID'] = strip(aline.split('agent_id=')[1])
                    break

    except Exception, e:
        logger.error("read_settings method failed! err_msg : {}".format(str(e.message)))
        return False, str(e.message)

    return True, server


def getinfo(to, api, domain, port, method='GET'):
    """
    use httplib get api data
    :param to:
    :param api:
    :param domain:
    :param port:
    :param method
    :return:
    """
    httpclient = None
    obj = None

    if not httpdstate():  # the server already down
        return obj

    try:
        httpclient = httplib.HTTPConnection(domain, port, timeout=to)
        httpclient.request(method, api)

        # response is a HTTPResponse object
        response = httpclient.getresponse()
        if response.status == 200:
            obj = json.loads(response.read())
        else:
            logger.debug('method:getinfo -- {} {} {} {}'.format(method, api, str(response.status), response.reason))
    except Exception:
        error_msg0 = str(sys.exc_info()[0])
        error_msg1 = str(sys.exc_info()[1])
        logger.error("method:getinfo -- {}:{}{} {}{}".format(domain, str(port), api, error_msg0, error_msg1))
    finally:
        if httpclient:
            httpclient.close()
        return obj


def getAgentId():
    agent_settings_path = "{}{}".format(settings.BASE_DIR, '/uniagent.ini')
    agentid = ''
    try:
        with open(agent_settings_path) as settingsInfo:
            lines = settingsInfo.readlines()
            for line in lines:
                if strip(line).startswith("agent_id="):
                    agentid = strip(line.split('agent_id=')[1])
    except Exception, e:
        logger.error("getAgentId method failed! err_msg : {}".format(str(e.message)))
        return False, str(e.message)
    return True, agentid


def getRabbitmqIp():
    agent_settings_path = "{}{}".format(settings.BASE_DIR, '/uniserver.ini')
    agentid = ''
    try:
        with open(agent_settings_path) as settingsInfo:
            lines = settingsInfo.readlines()
            for line in lines:
                if strip(line).startswith("rabbitmq_ip="):
                    agentid = strip(line.split('rabbitmq_ip=')[1])
    except Exception, e:
        logger.error("getRabbitmqIp method failed! err_msg : {}".format(str(e.message)))
        return False, str(e.message)
    return True, agentid


def getServerInfo():
    server_settings_path = "{}{}".format(settings.BASE_DIR, '/uniserver.ini')
    server = {}
    try:
        with open(server_settings_path) as settingsInfo:
            lines = settingsInfo.readlines()
            for line in lines:
                if strip(line).startswith("server_ip="):
                    server['IP'] = strip(line.split('server_ip=')[1])
                elif strip(line).startswith("server_port="):
                    server['PORT'] = strip(line.split('server_port=')[1])
                elif strip(line).startswith("node_name="):
                    server['ALIAS'] = strip(line.split('node_name=')[1])
    except Exception, e:
        logger.error("getServerInfo method failed! err_msg : {}".format(str(e.message)))
        return False, str(e.message)
    return True, server


def postinfo(to, api, domain, port, params, method='POST'):
    """
    use httplib POST api data
    :param to:
    :param api:
    :param domain:
    :param port:
    :param params
    :param method
    :return:
    """
    httpclient = None
    obj = None

    if not httpdstate():  # the server already down
        return obj

    try:

        headers = {'Content-Type': 'application/json', 'Accept-encoding': 'gzip'}
        httpclient = httplib.HTTPConnection(domain, port, timeout=to)
        httpclient.request(method, api, params, headers)

        # response is a HTTPResponse object
        response = httpclient.getresponse()
        # if response.status == 200:
        #     obj = json.loads(response.read())
        # else:
        #     logger.debug('method:postinfo response status is not 200 -- {} {} {} {}'.format(method, api,
        #                                                                                     str(response.status),
        #                                                                                     response.reason))
        obj = response.status
        return obj
    except Exception:
        error_msg0 = str(sys.exc_info()[0])
        error_msg1 = str(sys.exc_info()[1])
        logger.error("method:postinfo Exception -- {}:{}{} {}{}".format(domain, str(port), api, error_msg0, error_msg1))
    finally:
        if httpclient:
            httpclient.close()
        return obj


def httpdstate():
    """
    get apache running state
    """
    output = commands.getoutput('systemctl is-active httpd')
    if output == 'active':
        return True
    else:
        return False
