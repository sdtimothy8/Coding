# coding=utf8
import django
import commands
import sys
import os
import pika
from util import getAgentId
import constr
from cpu import getcpuload
from cpu import getinterrupts
from cpu import getcpuinfo
from cpu import getpercpuinfo
from cpu import get_total_cpu_info
from cpu import get_cpu_temperature
import datetime
from disk import get_disk_io
from disk import get_disk_block
from mem import getmembasicinfo
from mem import getpaginfo
from mem import get_swap_info
from mem import get_slab_info
from mem import get_numastat_info
from mem import get_total_memory
from networkio import get_throughput_info
from networkio import get_iptrafic_info
from networkio import get_socket_info
from networkio import get_tcp_info
from networkio import get_udp_info
from networkio import get_network_io
from networkio import get_total_network
from psdiskinfo import get_ps_disk_info
from util import task_producer
from filesystem import getfs
from process import get_ps_basic_info
from process import get_ps_info
from sensors import get_fans, deal_cpu_sensor
from string import strip
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.scheduler import Scheduler
# from ksmp import logger
from util import getServerInfo, getRabbitmqIp
from util import exchange_producer
import logging
logging.basicConfig()
import fcntl
import time
scheduler = Scheduler()


def cpu_info_taks():
    # print "cpu info task start"
    cpu_dict = {"x-message-ttl": 60000}
    body = getcpuinfo()
    task_producer("cpuinfo", body, cpu_dict)

def cpu_info_task_rrd():
    history_body = get_total_cpu_info()
    exchange_producer("cpuinforrd", history_body, None)

def index_cpu_load_task():
    history_body = getcpuload()
    exchange_producer("indexcpuload", history_body, None)

def index_cpu_memory_task():
    history_body = getmembasicinfo()
    exchange_producer("indexmemory", history_body, None)   

def index_cpu_disk_task():
    history_body = get_disk_io()
    exchange_producer("indexdisk", history_body, None) 

def index_network_task():
    history_body = get_network_io()
    exchange_producer("indexnetwork", history_body, None)    


def cpu_load_task():
    # print "cpu load task start"
    cpu_dict = {"x-message-ttl": 60000}
    body = getcpuload()
    task_producer("cpuload", body, cpu_dict)
    # task_producer("cpuloadrrd", body, None)


def process_disk_info_task():
    # print "process disk task start"
    dict = {"x-message-ttl": 8000}
    body = get_ps_disk_info()
    exchange_producer("psdiskinfo", body, dict)


def cpu_interrupt_task():
    # print "cpu interrupt task start"
    cpu_dict = {"x-message-ttl": 12000}
    body = getinterrupts()
    task_producer("interrupt", body, cpu_dict)


def single_cpu_task():
    print "single cpu task start"
    cpu_dict = {"x-message-ttl": 60000}
    body = getpercpuinfo()
    task_producer("singlecpuinfo", body, cpu_dict)


def mem_basic_info_task():
    # print "mem info task start"
    dict = {"x-message-ttl": 60000}
    body = getmembasicinfo()
    task_producer("membaseinfo", body, dict)


def mem_basic_info_task_rrd():
    history_body = get_total_memory()
    exchange_producer("meminforrd", history_body, None)


def mem_page_task():
    # print "mem page task start"
    dict = {"x-message-ttl": 60000}
    body = getpaginfo()
    task_producer("mempage", body, dict)
    # task_producer("pageinforrd", body, None)


def mem_swap_task():
    # print "mem swap task start"
    dict = {"x-message-ttl": 60000}
    body = get_swap_info()
    task_producer("memswap", body, dict)
    # task_producer("swapinforrd", body, None)


def mem_slab_task():
    # print "mem slab task start"
    dict = {"x-message-ttl": 60000}
    body = get_slab_info()
    task_producer("memslab", body, dict)
    # task_producer("slabinforrd", body, None)


def mem_numstat_task():
    # print "mem numa task start"
    dict = {"x-message-ttl": 12000}
    body = get_numastat_info()
    task_producer("numstatinfo", body, dict)


def disk_io_task():
    # print "disk io task start"
    dict = {"x-message-ttl": 60000}
    body = get_disk_io()
    task_producer("diskinfo", body, dict)


def disk_io_task_rrd():
    body = get_disk_io()
    exchange_producer("diskiorrd", body, None)


def disk_block_task():
    # print "disk block task start"
    dict = {"x-message-ttl": 60000}
    body = get_disk_block()
    task_producer("diskblock", body, dict)


def network_throughput_task():
    # print "network throughput task start"
    dict = {"x-message-ttl": 60000}
    body = get_throughput_info()
    task_producer("networkthroughput", body, dict)


def network_throughput_task_rrd():
    history_body = get_total_network()
    exchange_producer("throughputinforrd", history_body, None)


def network_iptraffic_task():
    # print "ip traffic task start"
    dict = {"x-message-ttl": 60000}
    body = get_iptrafic_info()
    task_producer("networktraffic", body, dict)
    # task_producer("iptrafficrrd", body, None)


def network_tcp_task():
    # print "tcp task start"
    dict = {"x-message-ttl": 60000}
    body = get_tcp_info()
    task_producer("networktcp", body, dict)
    # task_producer("tcpinforrd", body, None)


def network_udp_task():
    # print "udp task start"
    dict = {"x-message-ttl": 60000}
    body = get_udp_info()
    task_producer("networkudp", body, dict)
    # task_producer("udpinforrd", body, None)


def network_socket_task():
    # print "socket task start"
    dict = {"x-message-ttl": 60000}
    body = get_socket_info()
    task_producer("networksocket", body, dict)
    # task_producer("socketinforrd", body, None)


def network_io_task():
    # print "network io task start"
    dict = {"x-message-ttl": 60000}
    body = get_network_io()
    task_producer("networkio", body, dict)


def fs_task():
    dict = {"x-message-ttl": 8000}
    body = getfs()
    exchange_producer("fs_queue", body, dict)


def process_info_task():
    dict = {"x-message-ttl": 8000}
    body = get_ps_basic_info()
    task_producer("processInfo_queue", body, dict)


def fans_task():
    dict = {"x-message-ttl": 60000}
    body = get_fans()
    task_producer("fun", body, dict)


def fans_task_rrd():
    body = get_fans()
    exchange_producer("fanrrd", body, None)


def sensor_task():
    dict = {"x-message-ttl": 60000}
    body = deal_cpu_sensor()
    task_producer("cputemper", body, dict)


# 预警信息采集
flag, agentId = getAgentId()
if not flag:
    agentId = ''


def alarm_task():
    # print "alarm task start"
    alarm_body = []
    alarm_body.extend(cpu_base_alarm())
    alarm_body.extend(cpu_load_alarm())
    alarm_body.extend(cpu_temperature_alarm())
    alarm_body.extend(mem_alarm())
    alarm_body.extend(swap_alarm())
    alarm_body.extend(fs_alarm())
    alarm_body.extend(pscpu_alarm())
    alarm_body.extend(psmem_alarm())
    task_producer("warningQueue", alarm_body, None)


# cpu负载预警采集
def cpu_load_alarm():
    data = getcpuload()
    min1 = {constr.WARNING_HOST: agentId,
            constr.WARNING_TYPE: constr.CPU_LOAD_1MIN,
            constr.WARNING_DATA: data['min1'],
            constr.WARNING_LOCATION: "",
            constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    min5 = {constr.WARNING_HOST: agentId,
            constr.WARNING_TYPE: constr.CPU_LOAD_5MIN,
            constr.WARNING_DATA: data['min5'],
            constr.WARNING_LOCATION: "",
            constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    min15 = {constr.WARNING_HOST: agentId,
             constr.WARNING_TYPE: constr.CPU_LOAD_15MIN,
             constr.WARNING_DATA: data['min15'],
             constr.WARNING_LOCATION: "",
             constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    body = [min1, min5, min15]
    return body


# cpu基本信息预警采集
def cpu_base_alarm():
    data = getcpuinfo()
    cpu_user = {constr.WARNING_HOST: agentId,
                constr.WARNING_TYPE: constr.CPU_USER,
                constr.WARNING_DATA: float(data['user'])/100,
                constr.WARNING_LOCATION: "",
                constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    cpu_system = {constr.WARNING_HOST: agentId,
                  constr.WARNING_TYPE: constr.CPU_SYSTEM,
                  constr.WARNING_DATA: float(data['system'])/100,
                  constr.WARNING_LOCATION: "",
                  constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    cpu_iowait = {constr.WARNING_HOST: agentId,
                  constr.WARNING_TYPE: constr.CPU_IOWAIT,
                  constr.WARNING_DATA: float(data['iowait'])/100,
                  constr.WARNING_LOCATION: "",
                  constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    body = [cpu_user, cpu_system, cpu_iowait]
    return body

# CPU温度采集
def cpu_temperature_alarm():
    data = get_cpu_temperature()
    if data is not None:
        body = []
        for cpusensor in data:
            cpu_id = cpusensor['label']
            if 'Physical' in strip(cpu_id):
                body.append(
                    {constr.WARNING_HOST: agentId,
                     constr.WARNING_TYPE: constr.CPU_TEMPERATURE,
                     constr.WARNING_DATA: float(cpusensor['value']),
                     constr.WARNING_LOCATION: cpu_id,
                     constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                )
    return body

# 内存预警采集
def mem_alarm():
    data = getmembasicinfo()
    warning_data = float(data['percent'])/100
    mem_percent = {constr.WARNING_HOST: agentId,
                   constr.WARNING_TYPE: constr.MEM_PHYSIC,
                   constr.WARNING_DATA: warning_data,
                   constr.WARNING_LOCATION: "",
                   constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    body = [mem_percent]
    return body


# swap预警采集
def swap_alarm():
    data = get_swap_info()
    warning_data = float(data['percent'])/100
    swap_percent = {
        constr.WARNING_HOST: agentId,
        constr.WARNING_TYPE: constr.MEM_SWAP,
        constr.WARNING_DATA: warning_data,
        constr.WARNING_LOCATION: "",
        constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    body = [swap_percent]
    return body


# 文件系统预警采集
def fs_alarm():
    fsList = getfs().get('body', [])

    body = []
    if fsList:
        for fsdata in fsList:
            if fsdata:
                warning_data = float(fsdata['percent'].replace('%', ''))/100
                location = fsdata['mntpoint'] + ' : ' + fsdata['devicename']
                # location = fsdata['fs_name']
                fs_percent = {
                    constr.WARNING_HOST: agentId,
                    constr.WARNING_TYPE: constr.FILESYSTEM,
                    constr.WARNING_DATA: warning_data,
                    constr.WARNING_LOCATION: location,
                    constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                body.append(fs_percent)
    return body


# 进程占用CPU比预警采集
def pscpu_alarm():
    data = get_ps_info('cpu')
    body = []
    if data:
        for pscpu in data:
            if pscpu:
                location = pscpu['name'] + '(' + pscpu['pid'] + ')'
                pscpu_data = {constr.WARNING_HOST: agentId,
                              constr.WARNING_TYPE: constr.PS_CPU_RATE,
                              constr.WARNING_DATA: float(pscpu['cpu'])/100,
                              constr.WARNING_LOCATION: location,
                              constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                body.append(pscpu_data)
    return body


# 进程占用内存比预警采集
def psmem_alarm():
    data = get_ps_info('memory')
    body = []
    if data:
        for psmem in data:
            if psmem:
                location = psmem['name'] + '(' + psmem['pid'] + ')'
                psmem_data = {constr.WARNING_HOST: agentId,
                              constr.WARNING_TYPE: constr.PS_MEM_RATE,
                              constr.WARNING_DATA: float(psmem['mem'])/100,
                              constr.WARNING_LOCATION: location,
                              constr.WARNING_TIME: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                body.append(psmem_data)
    return body


def httpdstate():
    """
    get apache running state
    """
    output = commands.getoutput('systemctl is-active httpd')
    if output == 'active':
        return True
    else:
        try:
            scheduler.shutdown()
        finally:
            logging.debug('The Apache Server is not running ! Task Stopped !')
            return False


def schedu():
    """
    task scheduler
    :return:
    """
    scheduler.add_interval_job(cpu_info_taks, seconds=3)
    scheduler.add_interval_job(cpu_info_task_rrd, seconds=10)
    scheduler.add_interval_job(cpu_interrupt_task, seconds=3)
    scheduler.add_interval_job(cpu_load_task, seconds=3)
    scheduler.add_interval_job(single_cpu_task, seconds=3)
    scheduler.add_interval_job(index_cpu_load_task, seconds=3)

    scheduler.add_interval_job(mem_basic_info_task, seconds=3)
    scheduler.add_interval_job(mem_basic_info_task_rrd, seconds=10)
    scheduler.add_interval_job(mem_page_task, seconds=3)
    scheduler.add_interval_job(mem_swap_task, seconds=3)
    scheduler.add_interval_job(mem_slab_task, seconds=3)
    scheduler.add_interval_job(mem_numstat_task, seconds=3)
    scheduler.add_interval_job(index_cpu_memory_task, seconds=3)

    scheduler.add_interval_job(network_throughput_task, seconds=3)
    scheduler.add_interval_job(network_throughput_task_rrd, seconds=10)
    scheduler.add_interval_job(network_iptraffic_task, seconds=3)
    scheduler.add_interval_job(network_socket_task, seconds=3)
    scheduler.add_interval_job(network_tcp_task, seconds=3)
    scheduler.add_interval_job(network_udp_task, seconds=3)
    scheduler.add_interval_job(index_network_task, seconds=3)


    scheduler.add_interval_job(disk_io_task, seconds=3)
    scheduler.add_interval_job(disk_io_task_rrd, seconds=10)
    scheduler.add_interval_job(disk_block_task, seconds=3)
    scheduler.add_interval_job(index_cpu_disk_task, seconds=3)
    
    scheduler.add_interval_job(fs_task, seconds=3)
    scheduler.add_interval_job(process_info_task, seconds=3)
    scheduler.add_interval_job(process_disk_info_task, seconds=8)

    scheduler.add_interval_job(fans_task, seconds=3)
    scheduler.add_interval_job(fans_task_rrd, seconds=10)
    scheduler.add_interval_job(sensor_task, seconds=3)
    scheduler.add_interval_job(network_io_task, seconds=3)

    scheduler.add_interval_job(alarm_task, seconds=60)
    scheduler.start()


def pause_task(task):
    """
    pause some tasks
    :param task:
    :return:
    """
    list_task = get_jobs()
    if task == "cpu":
        if "cpu_info_taks" in list_task:
            scheduler.unschedule_func(cpu_info_taks)
        if "cpu_info_task_rrd" in list_task:
            scheduler.unschedule_func(cpu_info_task_rrd)
        if "cpu_interrupt_task" in list_task:
            scheduler.unschedule_func(cpu_interrupt_task)
        if "cpu_load_task" in list_task:
            scheduler.unschedule_func(cpu_load_task)
        if "single_cpu_task" in list_task:
            scheduler.unschedule_func(single_cpu_task)
        if "index_cpu_load_task" in list_task:
            scheduler.unschedule_func(index_cpu_load_task)
    elif task == "mem":
        if "mem_basic_info_task" in list_task:
            scheduler.unschedule_func(mem_basic_info_task)
        if "mem_basic_info_task_rrd" in list_task:
            scheduler.unschedule_func(mem_basic_info_task_rrd)
        if "mem_page_task" in list_task:
            scheduler.unschedule_func(mem_page_task)
        if "mem_swap_task" in list_task:
            scheduler.unschedule_func(mem_swap_task)
        if "mem_slab_task" in list_task:
            scheduler.unschedule_func(mem_slab_task)
        if "mem_numstat_task" in list_task:
            scheduler.unschedule_func(mem_numstat_task)
        if "index_cpu_memory_task" in list_task:
            scheduler.unschedule_func(index_cpu_memory_task)
    elif task == "net":
        if "network_throughput_task" in list_task:
            scheduler.unschedule_func(network_throughput_task)
        if "network_throughput_task_rrd" in list_task:
            scheduler.unschedule_func(network_throughput_task_rrd)
        if "network_iptraffic_task" in list_task:
            scheduler.unschedule_func(network_iptraffic_task)
        if "network_socket_task" in list_task:
            scheduler.unschedule_func(network_socket_task)
        if "network_tcp_task" in list_task:
            scheduler.unschedule_func(network_tcp_task)
        if "network_udp_task" in list_task:
            scheduler.unschedule_func(network_udp_task)
        if "network_io_task" in list_task:
            scheduler.unschedule_func(network_io_task)
        if "index_network_task" in list_task:
            scheduler.unschedule_func(index_network_task)
    elif task == "disk":
        if "disk_io_task" in list_task:
            scheduler.unschedule_func(disk_io_task)
        if "disk_io_task_rrd" in list_task:
            scheduler.unschedule_func(disk_io_task_rrd)
        if "disk_block_task" in list_task:
            scheduler.unschedule_func(disk_block_task)
        if "index_cpu_disk_task" in list_task:
            scheduler.unschedule_func(index_cpu_disk_task)
    elif task == "file":
        if "fs_task" in list_task:
            scheduler.unschedule_func(fs_task)
    elif task == "proc":
        if "process_info_task" in list_task:
            scheduler.unschedule_func(process_info_task)
    elif task == "trans":
        if "fans_task" in list_task:
            scheduler.unschedule_func(fans_task)
        if "fans_task_rrd" in list_task:
            scheduler.unschedule_func(fans_task_rrd)
        if "sensor_task" in list_task:
            scheduler.unschedule_func(sensor_task)
    elif task == "basic":
        if "index_cpu_memory_task" in list_task:
            scheduler.unschedule_func(index_cpu_memory_task)
        if "index_cpu_load_task" in list_task:
            scheduler.unschedule_func(index_cpu_load_task)
        if "index_network_task" in list_task:
            scheduler.unschedule_func(index_network_task)
        if "index_cpu_disk_task" in list_task:
            scheduler.unschedule_func(index_cpu_disk_task)


def resume_task(task):
    """
    resume some task
    :param task:
    :return:
    """
    list_task = get_jobs()
    if task == "cpu":
        if "cpu_info_taks" not in list_task:
            scheduler.add_interval_job(cpu_info_taks, seconds=3)
        if "cpu_info_task_rrd" not in list_task:
            scheduler.add_interval_job(cpu_info_task_rrd, seconds=10)
        if "cpu_interrupt_task" not in list_task:
            scheduler.add_interval_job(cpu_interrupt_task, seconds=3)
        if "cpu_load_task" not in list_task:
            scheduler.add_interval_job(cpu_load_task, seconds=3)
        if "single_cpu_task" not in list_task:
            scheduler.add_interval_job(single_cpu_task, seconds=3)
        if "index_cpu_load_task" not in list_task:
            scheduler.add_interval_job(index_cpu_load_task, seconds=3)
    elif task == "mem":
        if "mem_basic_info_task" not in list_task:
            scheduler.add_interval_job(mem_basic_info_task, seconds=3)
        if "mem_basic_info_task_rrd" not in list_task:
            scheduler.add_interval_job(mem_basic_info_task_rrd, seconds=10)
        if "mem_page_task" not in list_task:
            scheduler.add_interval_job(mem_page_task, seconds=3)
        if "mem_swap_task" not in list_task:
            scheduler.add_interval_job(mem_swap_task, seconds=3)
        if "mem_slab_task" not in list_task:
            scheduler.add_interval_job(mem_slab_task, seconds=3)
        if "mem_numstat_task" not in list_task:
            scheduler.add_interval_job(mem_numstat_task, seconds=3)
        if "index_cpu_memory_task" not in list_task:
            scheduler.add_interval_job(index_cpu_memory_task, seconds=3)
    elif task == "net":
        if "network_throughput_task" not in list_task:
            scheduler.add_interval_job(network_throughput_task, seconds=3)
        if "network_throughput_task_rrd" not in list_task:
            scheduler.add_interval_job(network_throughput_task_rrd, seconds=10)
        if "network_iptraffic_task" not in list_task:
            scheduler.add_interval_job(network_iptraffic_task, seconds=3)
        if "network_socket_task" not in list_task:
            scheduler.add_interval_job(network_socket_task, seconds=3)
        if "network_tcp_task" not in list_task:
            scheduler.add_interval_job(network_tcp_task, seconds=3)
        if "network_udp_task" not in list_task:
            scheduler.add_interval_job(network_udp_task, seconds=3)
        if "network_io_task" not in list_task:
            scheduler.add_interval_job(network_io_task, seconds=3)
        if "index_network_task" not in list_task:
            scheduler.add_interval_job(index_network_task, seconds=3)
    elif task == "disk":
        if "disk_io_task" not in list_task:
            scheduler.add_interval_job(disk_io_task, seconds=3)
        if "disk_io_task_rrd" not in list_task:
            scheduler.add_interval_job(disk_io_task_rrd, seconds=10)
        if "disk_block_task" not in list_task:
            scheduler.add_interval_job(disk_block_task, seconds=3)
        if "index_cpu_disk_task" not in list_task:
            scheduler.add_interval_job(index_cpu_disk_task, seconds=3)
    elif task == "file":
        if "fs_task" not in list_task:
            scheduler.add_interval_job(fs_task, seconds=3)
    elif task == "proc":
        if "process_info_task" not in list_task:
            scheduler.add_interval_job(process_info_task, seconds=3)
        if "process_disk_info_task" not in list_task:
            scheduler.add_interval_job(process_disk_info_task, seconds=8)
    elif task == "trans":
        if "fans_task" not in list_task:
            scheduler.add_interval_job(fans_task, seconds=3)
        if "fans_task_rrd" not in list_task:
            scheduler.add_interval_job(fans_task_rrd, seconds=10)
        if "sensor_task" not in list_task:
            scheduler.add_interval_job(sensor_task, seconds=3)
    elif task == "basic":
        if "index_cpu_load_task" not in list_task:
            scheduler.add_interval_job(index_cpu_load_task, seconds=3)
        if "index_cpu_memory_task" not in list_task:
            scheduler.add_interval_job(index_cpu_memory_task, seconds=3)
        if "index_network_task" not in list_task:
            scheduler.add_interval_job(index_network_task, seconds=3)
        if "index_cpu_disk_task" not in list_task:
            scheduler.add_interval_job(index_cpu_disk_task, seconds=3)


def get_jobs():
    list = []
    task = []
    list = scheduler.get_jobs()
    for l in list:
        print l
        s = str(l).split(" (trigger")
        re = s[0]
        task.append(re)
    return task

def setting_consumer():
    """
    monitor setting operation
    :return:
    """
    credentials = pika.PlainCredentials('inspur', 'inspur')
    # flag, server = getServerInfo()
    flag, ip = getRabbitmqIp()
    exchange_name = "monitor_setting"
    try:
        print "consumer start"
        parameters = pika.ConnectionParameters(ip, 5672, '/', credentials)
        # parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, type="fanout")
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        # channel.queue_declare(queue='config', durable=True)

        print ' [*] Waiting for messages. To exit press CTRL+C'

        def callback(ch, method, properties, body):
            print " [x] Received %r" % (body,)
            str = body
            list = str.split(":")
            print list
            if list[1] == "off":
                print get_jobs()
                pause_task(list[0])
                print list[0]+" task is stop"
                print get_jobs()
            else:
                print get_jobs()
                resume_task(list[0])
                print list[0]+" task is resume"
                print get_jobs()
            # channel.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

        channel.start_consuming()
    except Exception, e:
        print "except error!!!!!!!!!!!!!!!!!!!"
        logging.error("except error!!")
        time.sleep(10)
        setting_consumer()


def task_scheduler():
    try:
        schedu()
    except:
        time.sleep(10)
        task_scheduler()

if __name__ == "__main__":
    try:
        pid_path = sys.path[0] + '/task.pid'
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
    print "task scheduler is start!"
    task_scheduler()
    setting_consumer()