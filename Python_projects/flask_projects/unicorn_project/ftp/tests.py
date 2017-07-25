#!/usr/bin/python

import json
from django.test import TestCase
import mock


class VsftpdStatusTests(TestCase):
    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        """
        The status of test for FTP service
        """
        mock_cmd.return_value = (0, "success")
        response = self.client.get("/ftp/")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/ftp/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_put(self, mock_cmd):
        """
        Modify the state of the FTP service test
        """
        test_status = {"status": "1"}
        putdata = json.dumps(test_status)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.put("/ftp/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.put("/ftp/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        test_status = {"status": "0"}
        putdata = json.dumps(test_status)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.put("/ftp/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.put("/ftp/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)


class VsftpdLinksTests(TestCase):
    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        """
        The test for the FTP link information
        """
        mock_cmd.return_value = (0, "tcp        0        0        0.0.0.0:21        0.0.0.0:*        LISTEN        5448/vsftpd")
        response = self.client.get("/ftp/links")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "")
        response = self.client.get("/ftp/links")
        self.assertEqual(response.status_code, 200)


class UserTests(TestCase):
    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        """
        Test for the FTP user list
        """
        mock_cmd.return_value = (0, "success")
        response = self.client.get("/ftp/user")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_delete(self, mock_cmd):
        """
        Delete FTP user testing
        """
        test_user = {
            "name": "test",
            "homedir": "/var/ftp/test"
            }
        mock_cmd.return_value = (0, "success")
        deletedata = json.dumps(test_user)
        response = self.client.delete("/ftp/user", data=deletedata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.delete("/ftp/user", data=deletedata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_post(self):
        """
        Add FTP user testing
        """
        test_user = {
            "name": "test",
            "homedir": "/var/ftp/test",
            "passwd": "123456",
            "virtual_use_local_privs": "NO",
            "write_enable": "YES",
            "anon_world_readable_only": "NO",
            "anon_upload_enable": "NO",
            "anon_mkdir_write_enable": "NO",
            "anon_other_write_enable": "NO",
            "idle_session_timeout": 120,
            "data_connection_timeout": 120,
            "max_clients": 0,
            "max_per_ip": 0
            }
        test_user_1 = {
            "name": "test",
            "homedir": "/var/ftp/test"
            }
        deletedata = json.dumps(test_user_1)
        response = self.client.delete("/ftp/user", data=deletedata, content_type="application/json")
        postdata = json.dumps(test_user)
        response = self.client.post("/ftp/user", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/ftp/user", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)


class UserInfoTest(TestCase):
    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        """
        Test the query FTP user configuration information
        """

        mock_cmd.return_value = (0, "success")
        response = self.client.get("/ftp/userinfo/test")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/ftp/userinfo/test")
        self.assertEqual(response.status_code, 500)


class UserConfigTest(TestCase):

    def test_put(self):
        """
        Test modified FTP user configuration information
        """
        userconfig = {}
        putdata = json.dumps(userconfig)
        response = self.client.put("/ftp/userconfig", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        userconfig = {
            "name": "test",
            "new_passwd": "11111",
            "write_enable": "NO",
            "max_per_ip": "15"
            }
        putdata = json.dumps(userconfig)
        response = self.client.put("/ftp/userconfig", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class FTPConfigTest(TestCase):
    def test_get(self):
        """
        The test of FTP service configuration information
        """
        response = self.client.get("/ftp/ftpconfig/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_put(self, mock_cmd):
        """
        Test modified FTP service configuration information
        """
        putftpconfig = {
                "write_enable": "YES",
            }
        putdata = json.dumps(putftpconfig)
        mock_cmd.return_value = (0, "success")
        response = self.client.put("/ftp/ftpconfig/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = (1, "failed")
        response = self.client.put("/ftp/ftpconfig/", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)


class IPLimitTest(TestCase):

    def test_get(self):
        """
        The test for limit access to the IP address of the FTP server
        """
        response = self.client.get("/ftp/iplimit")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """
        Add testing limit access to the IP address of the FTP service information
        """
        ip_data = {"ip": "300.168.100.100.100"}
        postdata = json.dumps(ip_data)
        response = self.client.post("/ftp/iplimit", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        ip_data = {"ip": "300.168.100.100"}
        postdata = json.dumps(ip_data)
        response = self.client.post("/ftp/iplimit", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        ip_data = {"ip": "192.168.100.100"}
        postdata = json.dumps(ip_data)
        response = self.client.post("/ftp/iplimit", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        ip_data = {"ip": "192.168.200.0", "mask": "255.255.0.0"}
        postdata = json.dumps(ip_data)
        response = self.client.post("/ftp/iplimit", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/ftp/iplimit", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_put(self):
        """
        Test modified limit access to the IP address of the FTP service information
        """
        ip_data = {"old_ip": "192.168.100.100", "new_ip": "192.168.100.200"}
        putdata = json.dumps(ip_data)
        response = self.client.put("/ftp/iplimit", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        ip_data = {"old_ip": "192.168.100.200", "new_ip": "192.168.300.200"}
        putdata = json.dumps(ip_data)
        response = self.client.put("/ftp/iplimit", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        ip_data = {"old_ip": "192.168.200.0", "old_mask": "255.255.0.0", "new_ip": "192.168.210.0", "new_mask": "255.255.255.0"}
        putdata = json.dumps(ip_data)
        response = self.client.put("/ftp/iplimit", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        ip_data = {"old_ip": "192.168.210.0", "old_mask": "255.255.255.0", "new_ip": "192.168.300.0", "new_mask": "255.255.255.0"}
        putdata = json.dumps(ip_data)
        response = self.client.put("/ftp/iplimit", data=putdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_delete(self):
        """
        Test delete limit access to the IP address of the FTP service
        """
        ip_data = {"ip": "192.168.100.200"}
        deletedata = json.dumps(ip_data)
        response = self.client.delete("/ftp/iplimit", data=deletedata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        ip_data = {"ip": "192.168.210.0", "mask": "255.255.255.0"}
        deletedata = json.dumps(ip_data)
        response = self.client.delete("/ftp/iplimit", data=deletedata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
