"""
this is a test module for TCP Wrapper APP test
"""
import json
from django.test import TestCase
from business import TcpBusiness
import mock
from mock import call, patch

__author__ = 'zhuysh@inspur.com'

# Create your tests here.


class TestTcpCase(TestCase):

    @mock.patch('business.functions.launchcmd')
    def test_getlistinfo(self, mock_launchcmd):
        """
        test the GET method
        :param mock_launchcmd:
        :return:
        """

        file_object = open('thefile', 'w')
        file_object.write("abc:ALL:deny")
        file_object.close()
        mock_launchcmd.return_value = open("thefile", 'r')

        reference = TcpBusiness()

        ret_list = reference.getlistinfo("/etc/hosts.deny")

        self.assertListEqual(ret_list[0], ["abc", "ALL", "deny"])

        file_object2 = open('thefile2', 'w')
        file_object2.write("abc:ALL")
        file_object2.close()
        mock_launchcmd.return_value = open("thefile2", 'r')

        ret_list2 = reference.getlistinfo("/etc/hosts.deny")
        self.assertListEqual(ret_list2[0], ["abc", "ALL", "none"])

        file_object3 = open('thefile3', 'w')
        file_object3.write("abc")
        file_object3.close()
        mock_launchcmd.return_value = open("thefile3", 'r')

        ret_list3 = reference.getlistinfo("/etc/hosts.deny")
        self.assertListEqual(ret_list3[0], ["abc", "", "none"])

    @mock.patch('__builtin__.open')
    def test_putlistinfo(self, mock_open):
        """
        test the add method
        :param mock_open:
        :return:
        """

        test_data = {
            "addInfo": {
                "daemon": "ahayou",
                "hosts": "ALL",
                "command": "deny"
            }
        }
        post_data = json.dumps(test_data)

        mock_open.return_value = open('testfiel', 'a')

        response = self.client.post("/tcp/deny/", data=post_data, content_type="application/json")

        # print mock_open.return_value.method_calls == [call.write('ahayou:ALL:deny\n'), call.close()]
        # print mock_open.return_value.method_calls
        self.assertListEqual(mock_open.return_value.method_calls, [call.write('ahayou:ALL:deny\n'), call.close()])
        self.assertEqual(response.status_code, 200)

    # @mock.patch('__builtin__.open')
    @mock.patch('business.functions.launchcmd')
    def test_deletelistinfo(self, mock_launchcmd):
        """
        test the delete method
        :param mock_launchcmd:
        :return:
        """

        test_data = {"deleteinfo": ["aa,ALL,deny"]}
        post_data = json.dumps(test_data)

        file_object = open('thefile5', 'w')
        file_object.write("# test\naa:ALL:deny")
        file_object.close()

        mock_launchcmd.return_value = open("thefile5", 'r')
        with patch('__builtin__.open'):
            mock_open = open('thefile5', 'w+')
            response = self.client.delete("/tcp/deny/", data=post_data, content_type="application/json")
            # print mock_open.method_calls
            self.assertListEqual(mock_open.method_calls, [call.writelines(['# test\n']), call.close()])
            self.assertEqual(response.status_code, 200)
