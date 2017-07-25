# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

"""
this module provide tests for VM Manager.
"""
from django.test import TestCase
import json
from mock import patch

__author__ = 'shanchaobj@inspur.com'


class TestCreatorCase(TestCase):

    def test_getsuggestion(self):
        self.client.get("/vmmanager/creator/")
        self.assertEqual(response.status_code, 200)

    @patch("create.VMCreator.detect_os")
    def test_getosinfo(self, mock_os):
        mock_os.return_value = ("CentOS 7.0", "Linux")
        test_data = {"vm_iso_path": "/home/vagary/Downloads/cent7.iso"}
        post_data = json.dumps(test_data)
        self.client.post("/vmmanager/creator/",
                         data=post_data,
                         content_type="application/json")
        self.assertEqual(response.status_code, 200)


class TestVMCase(TestCase):

    def test_createvm(self):
        test_data = {"vm_name": "kux_vm",
                     "vm_iso_path": "/home/vagary/Downloads/cent7.iso",
                     "vm_install_method": 1, "vm_cpu": 1,
                     "vm_mem": 1024, "vm_storage_size": 10}
        post_data = json.dumps(test_data)
        response = self.client.post("/vmmanager/vm/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/vmmanager/vm/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_getvm(self):
        test_data = {"vm_name": "kux_vm"}
        test_data2 = {"vm_name": "kux_vm_noexist"}
        self.client.get("/vmmanager/vm/", data=test_data)
        self.assertEqual(response.status_code, 200)
        self.client.get("/vmmanager/vm/", data=test_data2)
        self.assertEqual(response.status_code, 400)


class TestVMsCase(TestCase):

    def test_getvmlist(self):
        response = self.client.get("/vmmanager/vms/")
        self.assertEqual(response.status_code, 200)


class TestLifecycleCase(TestCase):

    def test_lifecycle(self):
        test_data = {"vm_list": ["kux_vm"], "vm_status": "shutdown"}
        test_data2 = {"vm_list": ["kux_vm", "kux_vm_noexist"],
                      "vm_status": "shutdown"}
        post_data = json.dumps(test_data)
        response = self.client.post("/vmmanager/lifecycle/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        post_data = json.dumps(test_data2)
        response = self.client.post("/vmmanager/lifecycle/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)


class TestRemoveCase(TestCase):

    def test_remove(self):
        test_data = {"vm_list": ["kux_vm"]}
        post_data = json.dumps(test_data)
        response = self.client.post("/vmmanager/remove/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/vmmanager/remove/",
                                    data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
