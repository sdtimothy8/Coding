#!/usr/bin/python
#coding:utf-8
from flask import Flask, jsonify, request
from flask import Blueprint, abort
import os
import threading
import time
import util

ServiceManagementRoute = Blueprint('ServiceManagement', __name__)
Service_dict = {}
Service_blacklist = []

# Get all Services
@ServiceManagementRoute.route('/services')
def get_services():
    """
    return: the services list include basic information
    """
    result_list = util.getServiceList()
    return jsonify({'ServicesInfo': result_list})

# Quiery Service
@ServiceManagementRoute.route('/services/quiery')
def quiery_service():
    """
    Quiery the service info based on the search conditions.
    """
    if not request.json:
        abort(404)

    serviceName = request.json.get("serviceName", "")
    status = request.json.get("status", "")

    result_list = util.getConditionalServiceList(serviceName, status)
    return jsonify({"Quiery service info": result_list})

# Start or stop Service
@ServiceManagementRoute.route('/services/start', methods=['GET'])
def start_service():
    """
    Start the Service
    """
    serviceName = request.json.get("serviceName", "")
    if len(serviceName) == 0:
        abort(404)

    cmd = "systemctl start " + serviceName
    os.system(cmd)
    return jsonify({'Start service': "successfully!"})
 
@ServiceManagementRoute.route('/services/stop', methods=['GET'])
def stop_service():
    """
    Stop the Service
    """
    serviceName = request.json.get("serviceName", "")
    if len(serviceName) == 0:
        abort(404)

    cmd = "systemctl stop " + serviceName
    os.system(cmd)
    return jsonify({'Stop service': "successfully!"})

@ServiceManagementRoute.route('/services/enable', methods=['GET'])
def enable_service():
    """
    Enable the Service
    """
    serviceName = request.json.get("serviceName", "")
    if len(serviceName) == 0:
        abort(404)

    cmd = "systemctl enable " + serviceName
    os.system(cmd)
    return jsonify({'Enable service': "successfully!"})
   
@ServiceManagementRoute.route('/services/disable', methods=['GET'])
def disable_service():
    """
    Disable the Service
    """
    serviceName = request.json.get("serviceName", "")
    if len(serviceName) == 0:
        abort(404)

    cmd = "systemctl disable " + serviceName
    os.system(cmd)
    return jsonify({'Disable service': "successfully!"})
 
# Refresh the system Services
@ServiceManagementRoute.route('/services/refresh', methods=['GET'])
def refresh_Service():
    """
    Refresh the Services
    """
    service_list = util.getServiceList()
    return jsonify({'freshedServicesInfo': service_list})


# Add Services into self-control stratergy
@ServiceManagementRoute.route('/Services/stratergy', methods=['GET'])
def add_Service_into_self_stratergy():
    return jsonify({'stratergy': Service_list})



if __name__ == '__main__':
	app = Flask(__name__)
	app.register_blueprint(ServiceManagementRoute, url_prefix='')
	app.run(host = '0.0.0.0', port=8080)
