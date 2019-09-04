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

PortManagementRoute = Blueprint('PortManagement', __name__)

# Get all ports
@PortManagementRoute.route('/ports')
def get_ports():
    """
    return: the ports list include basic information
    """
    result_list = util.getAllPortsInfo()
    return jsonify({'portsInfo': result_list})

# Quiery port
@PortManagementRoute.route('/ports/quiery', methods=['GET'])
def quiery_port():
    portType = request.json.get('portType', "")
    portID = request.json.get('portID', "")
    status = request.json.get('status', "")
    result_list = util.getConditionalPortsInfo(portType, portID, status)
    return jsonify({"Conditional port": result_list})

# Open or close port
@PortManagementRoute.route('/ports/off/<string:portID>')
def close_port(portID):
    """
    Close the the port
    """
    cmd = 'iptables -I INPUT -p tcp --dport ' + portID + ' -j DROP'
    os.system(cmd)
    return jsonify({'Drop port': 'Done'})

# Open port
@PortManagementRoute.route('/ports/open/<string:portID>')
def open_port(portID):
    """
    Open the the port
    """
    cmd = 'iptables -I INPUT -p tcp --dport ' + portID + ' -j ACCEPT'
    os.system(cmd)
    return jsonify({'Accept port': 'Done'})
   

# Refresh the system ports
@PortManagementRoute.route('/ports/refresh', methods=['GET'])
def refresh_port():
    """
    Refresh the ports
    """
    port_list = util.getAllPortsInfo()
    return jsonify({'freshedPortsInfo': port_list})


# Add new port info
@PortManagementRoute.route('/ports', methods=['POST'])
def add_new_port():
    if not request.json or not 'portID' in request.json:
        abort(404)

    if not 'portID' in request.json:
        abort(404)

    if not 'portType' in request.json:
        abort(404)

    task = {
            'portID': request.json['portID'],
            'portType': request.json['portType'],
            'status': request.json.get('status', "")
            }
    port_list = util.getAllPortsInfo()
    port_list.append(task)
    return jsonify({'Result': port_list}), 201

# Add ports into self-control stratergy
@PortManagementRoute.route('/ports/stratergy', methods=['GET'])
def add_port_into_self_stratergy():
    return jsonify({'stratergy': port_list})



if __name__ == '__main__':
	app = Flask(__name__)
	app.register_blueprint(PortManagementRoute, url_prefix='')
	app.run(host = '0.0.0.0', port=8080)
