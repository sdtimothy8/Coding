#!/usr/bin/python
#coding:utf-8
from flask import Flask, jsonify, request
from flask import Blueprint, abort
import os
import threading
import time
import re
import psutil
import util

ProcessManagementRoute = Blueprint('ProcessManagement', __name__)
process_dict = {}
process_blacklist = []

# Get all processes
@ProcessManagementRoute.route('/processes')
def get_processes():
    """
    return:the process list  include basic information
    """
    result_list = util.getAllProcesses()
    return jsonify({'ProcessInfo': result_list})

# Quiery process
@ProcessManagementRoute.route('/processes/quiery', methods=['GET'])
def quiery_process():
    """
    Search the process based on the quiery condition
    """
    userName = request.json.get('userName', "")
    processPid = request.json.get('processPid', "")
    program = request.json.get('cmd', "")
    result_list = util.getConditionalProcesses( userName, processPid, program )

    return jsonify({'Conditional process': result_list})

# Close the process
@ProcessManagementRoute.route('/processes/off/<string:pid>')
def close_process(pid):
    """
    Close the the process
    """
    # Here need consider the important system process
    cmd = 'kill -9 ' + pid
    print cmd
    os.system(cmd)
    result_list = util.getAllProcesses()
    return jsonify({'ProcessInfo': result_list})

# Hide some system processes
@ProcessManagementRoute.route('/processes/hidden', methods=['GET'])
def hidden_process():
    """
    Hidden the processes in the process_backlist
    """
    process_list = util.getAllProcesses()
    for black_process in process_blacklist:
        black_pid = black_process['processPid']
        task = filter(lambda t: t['pid'] == black_pid, process_list)
        if len(task) != 0:
            process_list.remove(task[0])
    
    return jsonify({'hidden_process_list': process_list})


# Add new process info into process blacklist
@ProcessManagementRoute.route('/processes/blacklist/add', methods=['POST'])
def process_blacklist_add():
    if not request.json or not 'processPid' in request.json:
        abort(404)

    task = {
            'processPid': request.json['processPid'],
            'userName': request.json.get('userName', ""),
            'cmd': request.json.get('cmd', "")
            }

    process_blacklist.append(task)
    #return jsonify({'Result': True}), 201
    return jsonify({'Result': process_blacklist}), 201

# Delete process info from process blacklist
@ProcessManagementRoute.route('/processes/blacklist', methods=['GET'])
def get_process_blacklist():
    return jsonify({'process_backlist': process_blacklist})


# Remove process info from process blacklist
@ProcessManagementRoute.route('/processes/blacklist', methods=['DELETE'])
def process_backlist_remove():
    """
    Remove the specific processes from the process back list
    """
    if not request.json or not 'processPid' in request.json:
        abort(404)

    pid_list = request.json['processPid']
    for pid in pid_list:
        task = filter(lambda t: t['processPid'] == pid, process_blacklist)
        if len(task) == 0:
            abort(404)
        process_blacklist.remove(task[0])
    
    return jsonify({'process_backlist': process_blacklist})


if __name__ == '__main__':
	app = Flask(__name__)
	app.register_blueprint(ProcessManagementRoute, url_prefix='')
	app.run(host = '0.0.0.0', port=8080)
