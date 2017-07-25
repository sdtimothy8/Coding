"""
tests for module sysmonitor
"""
from django.test import TestCase
import mock
# Create your tests here.


class TestDiskViews(TestCase):
    """
    test for disk monitor
    """

    def test_readdiskIO(self):
        """
        test for disk monitor
        :return:
        """
        with mock.patch('sysmonitor.common.Common.command_exec') as mock_common:
            mock_common.return_value = True, "test"
            response = self.client.get("/monitor/disk/io/")
            mock_common.assert_called_with("sar -b 1 1", 1, 1, -1, {0: "time"})
            self.assertEqual(mock_common.call_count, 1)
            self.assertTrue(mock_common.called)
            self.assertEqual(response.status_code, 200)
            mock_common.return_value = False, "test"

            response = self.client.get("/monitor/disk/io/")
            self.assertEqual(mock_common.call_count, 2)
            self.assertEqual(response.status_code, 500)

            with mock.patch("sysmonitor.plugins.unicorn_disk_com.Plugin.join_iostat_to_sard")\
                    as mock_join:
                mock_common.return_value = True, "[{'time':123,'dev':'dev1'},{'time':456,'dev':'dev2'}]"
                mock_join.return_value = "test_join"
                response = self.client.get("/monitor/disk/block/")
                self.assertEqual(mock_common.call_count, 4)
                self.assertEqual(mock_join.call_count, 1)
                self.assertEqual(response.data, 'test_join')
                self.assertEqual(response.status_code, 200)
