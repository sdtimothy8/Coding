#!/usr/bin/python
#coding:utf-8
from flask import Flask, jsonify
from flask import Blueprint, abort
import os
import threading
import time
import re
import psutil
import util

ProcessManagementRoute = Blueprint('ProcessManagement', __name__)
process_dict = {}

# Get all processes
@ProcessManagementRoute.route('/processes')
def get_processes():
    """
    return:the process list  include basic information
    """
    result_list = util.getAllProcesses()
    return jsonify({'ProcessInfo': result_list})

# Quiery process
@ProcessManagementRoute.route('/processes/quiery')
def get_process(process_pid):
	return jsonify(process_dict)

# Close the process
@ProcessManagementRoute.route('/processes/off')
def close_process():
    pass

# Hide some system processes
@ProcessManagementRoute.route('/processes/hidden')
def hidden_process():
    pass

# process blacklist management
@ProcessManagementRoute.route('/processes/operation')
def process_operation():
    pass

if __name__ == '__main__':
	app = Flask(__name__)
	app.register_blueprint(ProcessManagementRoute, url_prefix='')
	you app.run(host = '0.0.0.0', port=8080)
