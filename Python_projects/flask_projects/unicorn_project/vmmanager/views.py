# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

"""
this module is for VMM(Virtual Machine Manager) Wrapper views_module
"""

from rest_framework.views import APIView
from rest_framework import status
# the old way to format Response message with following.
# from ksmp import message
# now rewrite it with the following.
from vmmanager.helper import *
# import default connection to system libvirt service.
from vmmanager.instance import get_conn
# import format reader to help output info.
from vmmanager.reader import VMFmtReader

from vmmanager.create import VMCreator

from vnc.VNCToken import VNCToken

__author__ = 'shanchaobj@inspur.com'

(INSTALL_METHOD_ISO,
 INSTALL_METHOD_URL,
 INSTALL_METHOD_PXE,
 INSTALL_METHOD_IMPORT,
 INSTALL_METHOD_CONTAINER_APP,
 INSTALL_METHOD_CONTAINER_OS) = range(6)


def _format_vm(vm, conn=None, v=False):
    """
    Format VMDomain information to a dict.
        v = True : verbose print detail info into dict.
    """
    vm_detail = {}
    vm_detail["vm_uuid"] = vm.get_uuid()
    vm_detail["vm_name"] = vm.get_name()
    vm_detail["vm_status"] = vm.run_status()
    if v:
        infoReader = VMFmtReader(vm, conn)
        vm_detail["vm_title"] = vm.get_title() or ""
        vm_detail["vm_description"] = vm.get_description() or ""
        vm_detail["vm_cpu"] = infoReader.cpu()
        vm_detail["vm_mem"] = infoReader.mem()
        # Hypervisor Details
        vm_detail["vm_hypervisor"] = infoReader.hv()
        # Storage
        vm_detail["vm_storages"] = infoReader.storages()
        # Network
        vm_detail["vm_networks"] = infoReader.networks()
    return vm_detail


class VMList(APIView):
    """
    VMList Wrappers VMM Domain list options
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "GET",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def get(self, request):
        """
        GET method: Get vm list
        """
        conn = get_conn()
        vms = conn.list_vms()
        vmlist = []
        for vm in vms:
            vmlist.append(_format_vm(vm))

        return Reply(RESPONSE_SUCCESS, data={"vms": vmlist},
                     status=status.HTTP_200_OK, CROS=True)


class VM(APIView):
    """
    VM Wrappers VMM Domain
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "GET,POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def get(self, request):
        """
        GET method: Get vm detail information
        """
        conn = get_conn()
        vm_name = request.GET.get("vm_name", None)
        if vm_name is None:
            return Reply(RESPONSE_ERROR, data="query_params is required",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)
        vm = conn.get_vm(vm_name)
        if vm is None:
            return Reply(RESPONSE_ERROR, data="vm '%s' not found" % vm_name,
                         status=status.HTTP_404_NOT_FOUND, CROS=True)

        return Reply(RESPONSE_SUCCESS, data=_format_vm(vm, conn, v=True),
                     status=status.HTTP_200_OK, CROS=True)

    def post(self, request):
        """
        POST method: Create a new vm
        """
        conn = get_conn()
        vm_name = request.data.get("vm_name", None)
        vm_install_method = request.data.get("vm_install_method", None)
        vm_iso_path = request.data.get("vm_iso_path", None)
        vm_os_type = request.data.get("vm_os_type", None)
        vm_os_version = request.data.get("vm_os_version", None)
        vm_cpu = request.data.get("vm_cpu", None)
        vm_mem = request.data.get("vm_mem", None)
        vm_storage_size = request.data.get("vm_storage_size", None)
        # raise no param provide
        if not vm_name or not vm_os_type or not vm_os_version or not (
            vm_iso_path or not vm_install_method) or not (
                vm_cpu or not vm_mem or not vm_storage_size):
            return Reply(RESPONSE_ERROR, data="query_params is required",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)
        # raise int param format invalid
        try:
            vm_install_method = int(vm_install_method)
            vm_cpu = int(vm_cpu)
            vm_mem = int(vm_mem)
            vm_storage_size = int(vm_storage_size)
        except Exception, e:
            return Reply(RESPONSE_ERROR, data="query_params is invalid",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)
        # TODO: debug mode auto response success
        # return Reply(RESPONSE_SUCCESS, data="debug mode ok",
        #              status=status.HTTP_200_OK, CROS=True)
        creator = VMCreator(conn)
        vm_port = VNCToken.get_now_port()
        message = creator.set_config(vm_name, vm_os_type,
                                     vm_os_version, vm_iso_path, vm_install_method,
                                     int(vm_cpu), int(vm_mem), int(vm_storage_size), int(vm_port))
        if message[0] is not True:
            errmsg = message[1] or ""
            return Reply(RESPONSE_ERROR, data="config vm faild." + errmsg,
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)

        # (xml, fxml) = creator.start_install_xml()
        # return Reply(RESPONSE_SUCCESS, data={"xml":xml,"fxml":fxml},
        #           status=status.HTTP_200_OK, CROS=True)
        (resstatus, result) = creator.start_install()
        if resstatus:
            VNCToken.save_token(result.get_uuid(), vm_port)
            return Reply(RESPONSE_SUCCESS,
                         data=_format_vm(result, conn, v=True),
                         status=status.HTTP_200_OK, CROS=True)

        return Reply(RESPONSE_ERROR, data="config vm faild.",
                     status=status.HTTP_500_INTERNAL_SERVER_ERROR, CROS=True)


class Lifecycle(APIView):
    """
    Lifecycle Wrappers Agent VMM Lifecycle
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def post(self, request):
        """
        POST method: Change vms lifecycle
        """
        conn = get_conn()
        vm_list = request.data.get("vm_list", [])
        if not len(vm_list) and "getlist" in dir(request.data):
            vm_list = request.data.getlist("vm_list[]", [])
        vm_status = request.data.get("vm_status", None)
        if not len(vm_list):
            return Reply(RESPONSE_ERROR, data="query_params is required",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)

        if not vm_status or (vm_status not in ["shutdown", "reboot", "destroy",
                             "reset", "startup", "suspend", "resume"]):
            return Reply(RESPONSE_ERROR, data="lifecycle status is invalid",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)
        vms = []
        for vm_name in vm_list:
            vm = conn.get_vm(vm_name)
            if vm is None:
                return Reply(RESPONSE_ERROR, data="query_params is invalid",
                             status=status.HTTP_400_BAD_REQUEST, CROS=True)
            vms.append(vm)
        for idx in range(len(vms)):
            try:
                getattr(vms[idx], vm_status)()
                vms[idx] = True
            except Exception, e:
                vms[idx] = e
        return Reply(RESPONSE_DONE, status=status.HTTP_200_OK, CROS=True)


class Remove(APIView):
    """
    Remove Wrappers Agent VMM Remove
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "GET,POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def post(self, request):
        """
        POST method: Remove a new vm "delete"
        """
        conn = get_conn()
        vm_list = request.data.get("vm_list", [])
        if not len(vm_list) and "getlist" in dir(request.data):
            vm_list = request.data.getlist("vm_list[]", [])
        if not len(vm_list):
            return Reply(RESPONSE_ERROR, data="query_params is required",
                         status=status.HTTP_400_BAD_REQUEST, CROS=True)
        vms = []
        for vm_name in vm_list:
            vm = conn.get_vm(vm_name)
            if vm is None:
                return Reply(RESPONSE_ERROR, data="query_params is invalid",
                             status=status.HTTP_400_BAD_REQUEST, CROS=True)
            vms.append(vm)
        for vm in vms:
            vm.delete()
        return Reply(RESPONSE_DONE, status=status.HTTP_200_OK, CROS=True)


class Creator(APIView):
    """
    Creator Wrappers Agent VMM Creator
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "GET,POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def get(self, request):
        conn = get_conn()
        vm_install_method = [
             ["install_method_iso", INSTALL_METHOD_ISO, 1],
             ["install_method_url", INSTALL_METHOD_URL, 0],
             ["install_method_pxe", INSTALL_METHOD_PXE, 0],
             ["install_method_import", INSTALL_METHOD_IMPORT, 0],
             ["install_method_container_app", INSTALL_METHOD_CONTAINER_APP, 0],
             ["install_method_container_o", INSTALL_METHOD_CONTAINER_OS, 0]
        ]
        vm_host_space = VMCreator.host_space(conn)
        vm_default_dir = VMCreator.default_dir(conn)
        return Reply(RESPONSE_SUCCESS, data={
                        "install_method": vm_install_method,
                        "host_cpu_count": conn.host_active_processor_count(),
                        "host_memory": int(round((conn.host_memory_size() / 1024))),
                        "host_space": vm_host_space,
                        "default_dir": vm_default_dir
                    }, status=status.HTTP_200_OK, CROS=True)

    def post(self, request):
        from vmmanager.create import _os_type_model, _os_variant_model
        return Reply(RESPONSE_SUCCESS, data={
                        "os_type": _os_type_model,
                        "os_version": _os_variant_model
                    }, status=status.HTTP_200_OK, CROS=True)


class Ip(APIView):
    """
    Ip Wrappers Agent Ip
    """
    def options(self, request):
        return Reply(RESPONSE_DONE, headers={
            "Access-Control-Allow-Method": "GET,POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
                request.META.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS", "*")
        })

    def get(self, request):
        import socket
        # 这个得到本地ip
        localIP = socket.gethostbyname(socket.gethostname())
        return Reply(RESPONSE_SUCCESS, data={"ip": localIP},
                     status=status.HTTP_200_OK, CROS=True)
