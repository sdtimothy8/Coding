"""
tests for module sysmonitor
"""
from django.test import TestCase
import mock
# Create your tests here.


class TestLogViews(TestCase):
    """
    test for log
    """
    @mock.patch('logmanager.service.LogDetailBusiness.view_logdetail_get')
    def test_readUnicorn(self, mock_unicorn):
        """
        test unicorn success
        :param mock_unicorn:
        :return:
        """
        return_update = True, []
        mock_unicorn.return_value = return_update
        response = self.client.get("/logmanager/unicorn/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('logmanager.service.LogDetailBusiness.view_logdetail_get')
    def test_readUnicornError(self, mock_unicorn):
        """
        test unicorn error
        :param mock_unicorn:
        :return:
        """
        return_update = False, []
        mock_unicorn.return_value = return_update
        response = self.client.get("/logmanager/unicorn/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 500)

    @mock.patch('logmanager.service.LogDetailBusiness.view_logdetail_get')
    def test_readKernel(self, mock_kernel):
        """
        test kernel log success
        :param mock_kernel:
        :return:
        """
        return_update = True, []
        mock_kernel.return_value = return_update
        response = self.client.get("/logmanager/kernel/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('logmanager.service.LogDetailBusiness.view_logdetail_get')
    def test_readKernelError(self, mock_kernel):

        """
        test kernel log error
        :param mock_kernel:
        :return:
        """
        return_update = False, []
        mock_kernel.return_value = return_update
        response = self.client.get("/logmanager/kernel/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 500)
