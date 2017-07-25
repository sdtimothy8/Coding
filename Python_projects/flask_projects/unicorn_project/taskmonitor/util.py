# __author__ = 'root'
import subprocess
import os
import pika
import json
from string import strip
import time
import sys
import traceback
import django
pro_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ksmp.settings'
django.setup()
from ksmp import logger

# import logging
# from ksmp import settings
# from ksmp import logger
# from agent.utils import getServerInfo


COMMON_NONE = 'comand is None!'
COMMON_EXCEPT = "except in command_exec, command= "


def launchcmd(cmdstr):
    """
    Launch a cmdstr, and get the result.
    :param cmdstr: command string.
    :return: The result after launching the cmdstr.
    """
    # Check if the input cmdstr is valid?
    pp = subprocess.Popen(cmdstr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    if pp:
        return pp.stdout


def command_exec(command, dict_flag=0, start=0, end=-1, changeKeys=None):
    """
    exec command then return; if dict_flag=0 return string list,if dict_flag=1 return dict list.
    when dict_flag=1, change string list from start to end.
    you can change the dict_key through diction changeKeys like {o:"time",2:"dev"}
    :param command:
    :param dict_flag:
    :param start:
    :param end:
    :param changeKeys:
    :return:
    """
    if command.strip() is None:
        return False, COMMON_NONE
    try:
        command_result = list_result_command(command)
        if 0 == dict_flag:
            return True, command_result
        command_dict_list = trans_list_to_dict(command_result, start, end, changeKeys)
    except:
        return False, COMMON_EXCEPT + command
    return True, command_dict_list


def list_result_command(command):
    """
    get list of commond , removed empty line
    """
    result_list = []
    list_com = os.popen(command).readlines()
    for line in list_com:
        if line.strip():
            result_list.append(line.strip())
    return result_list


def trans_list_to_dict(r_list, start=0, end=-1, changeKeys=None):
        """
        transform r_list to a list contain some dictionary
        trans from start to end
        satrt line is keys line
        trans all for end=-1
        change first key to changeFistKey except changeFistKey is None
        :param r_list:
        :param start:
        :param end:
        :param changeKeys:
        :return:
        """
        if end == -1:
            list_length = len(r_list)
        else:
            list_length = end

        list_keys = r_list[start].strip().split()
        if changeKeys is not None:
            for k, v in changeKeys.items():
                list_keys[k] = v

        key_length = len(list_keys)
        list_dict = []
        if key_length == 0:
            return list_dict
        for i in range(start+1, list_length):
            if len(r_list[i].strip()) == 0:
                continue
            line_i = r_list[i].strip().split()
            line_i_con = {}
            for j in range(0, key_length):
                line_i_con[list_keys[j]] = line_i[j]
            list_dict.append(line_i_con)
        return list_dict


def get_dict_by_name(dict_key, dict_name, dict_map):
        """
        get dict form dict_map when dict.dict_key = dict_name
        :param dict_key:
        :param dict_name:
        :param dict_map:
        :return:
        """
        for map in dict_map:
            if map[dict_key] == dict_name:
                return map
        return None


def get_index_by_name(dict_key, dict_name, dict_map):
        """
        get index form dict_map when dict.dict_key = dict_name
        :param dict_key:
        :param dict_name:
        :param dict_map:
        :return:
        """
        for i in range(0, len(dict_map)):
            if dict_map[i][dict_key] == dict_name:
                return i
        return -1

def getRabbitmqIp():
    agent_settings_path = "{}{}".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/uniserver.ini')
    agentid = ''
    try:
        with open(agent_settings_path) as settingsInfo:
            lines = settingsInfo.readlines()
            for line in lines:
                if strip(line).startswith("rabbitmq_ip="):
                    agentid = strip(line.split('rabbitmq_ip=')[1])
    except Exception, e:
        return False, str(e.message)
    return True, agentid


credentials = pika.PlainCredentials("inspur", "inspur")
flag, ip = getRabbitmqIp()
parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def task_producer(name, body, arguments):
    """

    :param name: queue name
    :param body: message body
    :return:
    """
    global connection
    global channel
    # credentials = pika.PlainCredentials("inspur", "inspur")
    # # flag, server = getServerInfo()
    # flag, ip = getRabbitmqIp()
    # # ip = server.get("IP")
    # parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
    # #  parameters = pika.ConnectionParameters(host="localhost", port=5672, virtual_host="/", credentials=credentials)
    # connection = pika.BlockingConnection(parameters)
    # channel = connection.channel()
    # channel.queue_declare(queue=name, durable=True, auto_delete=True, arguments=arguments)
    # body = json.dumps(body)
    # channel.basic_publish(exchange="", routing_key=name, body=body)
    # connection.close()
    try:
        send_message(name, body, arguments)
    except Exception as e:
        # logging.error(str(e.message))
        credentials = pika.PlainCredentials("inspur", "inspur")
        flag, ip = getRabbitmqIp()
        parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        logger.error("in taskmonitor --> " + str(e))
        logger.error("in taskmonitor --> " + traceback.print_exc())
        # logger.error("in taskmonitor --> send_message except occured.")
        #pass

def send_message(name, body, arguments):
    """
    send system message to rabbitmq server
    :return:
    """
    global connection
    global channel
    # credentials = pika.PlainCredentials("inspur", "inspur")
    ## flag, server = getServerInfo()
    # flag, ip = getRabbitmqIp()
    # logger.debug("in taskmonitor --> begin")
    ## ip = server.get("IP")
    # parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
    ##  parameters = pika.ConnectionParameters(host="localhost", port=5672, virtual_host="/", credentials=credentials)
    # connection = pika.BlockingConnection(parameters)
    if connection is None or not connection.is_open:
        credentials = pika.PlainCredentials("inspur", "inspur")
        flag, ip = getRabbitmqIp()
        parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
        connection = pika.BlockingConnection(parameters)
       
    # if connection is None:
    #    logger.error("in taskmonitor --> get connection error.")

    # if channel is not None:
    #    logger.info("in taskmonitor --> channel obtained.")
    # else:
    #    logger.error("in taskmonitor --> get channel error at channel open.")

    if channel is None or not channel.is_open:
        channel = connection.channel()

    #channel.queue_declare(queue=name, durable=True, auto_delete=True, arguments=arguments)
    body = json.dumps(body)
    channel.basic_publish(exchange="", routing_key=name, body=body)
    #logger.info("in taskmonitor --> data publish")
    #channel.close()
    #logger.info("in taskmonitor --> channel closed")
    #connection.close()
    #logger.info("in taskmonitor --> connection closed.")

def exchange_producer(name, body, arguments):
    """
    send message by direct exchange.
    :param name: queue name
    :param body: send message
    :param arguments: queue params
    :return:
    """
    global connection
    global channel
    try:
        #credentials = pika.PlainCredentials("inspur", "inspur")
        #flag, ip = getRabbitmqIp()
        #parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
        #connection = pika.BlockingConnection(parameters)
        #channel = connection.channel()
        #channel.exchange_declare(exchange="exchangeTest", type="direct", durable=True, auto_delete=False)
        # channel.queue_declare(queue=name, durable=True, auto_delete=True, arguments=arguments)
        if connection is None or not connection.is_open:
            credentials = pika.PlainCredentials("inspur", "inspur")
            flag, ip = getRabbitmqIp()
            parameters = pika.ConnectionParameters(host=ip, port=5672, virtual_host="/", credentials=credentials)
            connection = pika.BlockingConnection(parameters)
        if channel is None or not channel.is_open:
            channel = connection.channel()
        body = json.dumps(body)
        channel.basic_publish(exchange="exchangeTest", routing_key=name, body=body)
        # connection.close()
    except Exception as e:
        logger.error("in taskmonitor --> " + str(e.message))
        logger.error("in taskmonitor --> " + traceback.print_exc())
        pass


def getAgentId():
    agent_settings_path = "{}{}".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/uniagent.ini')
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


def getServerInfo():
    server_settings_path = "{}{}".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/uniserver.ini')
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



# if __name__ == "__main__":
#    flag, ip = getRabbitmqIp()
#    print ip
