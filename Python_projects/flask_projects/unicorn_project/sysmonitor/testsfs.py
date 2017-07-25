"""
tests for module sysmonitor
"""
from django.test import TestCase
import mock
# Create your tests here.


class TestFSViews(TestCase):
    """
    test for file system monitor
    """

    @mock.patch('sysmonitor.plugins.unicorn_sysfs.Plugin.update')
    def test_readfs(self, mock_fs):
        """
        test for file system monitor
        :param mock_fs:
        :return:
        """
        return_update = [{"mnt_point": "/",
                          "used": "11G",
                          "percent": "21%",
                          "free": "40G",
                          "device_name": "/dev/mapper/centos-root",
                          "size": "50G"
                          },
                         {"mnt_point": "/dev",
                          "used": "0",
                          "percent": "0%",
                          "free": "1.8G",
                          "device_name": "devtmpfs",
                          "size": "1.8G"
                          },
                         {"mnt_point": "/dev/shm",
                          "used": "488K",
                          "percent": "1%",
                          "free": "1.9G",
                          "device_name": "tmpfs",
                          "size": "1.9G"
                          }]
        # fs = mock.Mock(update=lambda: return_update)
        mock_fs.return_value = return_update
        response = self.client.get("/monitor/fs/basic/")
        self.assertEqual(response.data, return_update)
        self.assertEqual(response.status_code, 200)
