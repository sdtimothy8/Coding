"""
tests for module sysmonitor
"""
from django.test import TestCase
import mock
# Create your tests here.


class TestCpuViews(TestCase):
    """
    test for cpu monitor
    """

    @mock.patch('sysmonitor.plugins.unicorn_load.Plugin.update')
    def test_readCpuload(self, mock_load):
        """
        read cpu info
        :param mock_load:
        :return:
        """
        return_load = {"min1": 1.0,
                       "min5": 5.4,
                       "min15": 3.3,
                       "cpucore": 4}
        # load = mock.Mock(update=lambda: return_load)
        mock_load.return_value = return_load
        response = self.client.get("/monitor/cpu/load/")
        self.assertEqual(response.data, return_load)
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_cmd_sensor.Plugin.update')
    @mock.patch('sysmonitor.plugins.unicorn_percpu.Plugin.update')
    @mock.patch('sysmonitor.plugins.unicorn_cpu.Plugin.update')
    @mock.patch('sysmonitor.plugins.unicorn_load.Plugin.update')
    def test_readCpubase(self, mock_load, mock_cpu, mock_per, mock_sen):
        return_dic = {"min1": 1.0,
                      "min5": 5.4,
                      "min15": 3.3,
                      "cpucore": 4}
        re_baseinfo = {"softirq": 0.0,
                       "iowait": 1.4,
                       "system": 0.8}
        re_cpu = [{"cpu_number": 0,
                   "guest_nice": 0.0,
                   "softirq": 0.1
                   },
                  {"cpu_number": 1,
                   "guest_nice": 0.0,
                   "softirq": 0.0
                   }]
        re_sen = [{"value": "37.0",
                   "label": "Physical id 0"
                   },
                  {"value": "33.0",
                   "label": "Core 0"
                   },
                  {"value": "37.0",
                   "label": "Core 2"
                   }]
        # load = mock.Mock(update=lambda: return_dic)
        mock_load.return_value = return_dic
        # base = mock.Mock(update=lambda: re_baseinfo)
        mock_cpu.return_value = re_baseinfo
        # cpu_in = mock.Mock(update=lambda: re_cpu)
        mock_per.return_value = re_cpu
        # cpu_sen = mock.Mock(update=lambda: re_sen)
        mock_sen.return_value = re_sen
        # cpu baseinfo
        response = self.client.get("/monitor/cpu/baseinfo/")
        self.assertEqual(response.data, re_baseinfo)
        self.assertEqual(response.status_code, 200)
        # all cpu info
        response = self.client.get("/monitor/cpu/all/")
        self.assertEqual(response.data, re_cpu)
        self.assertEqual(response.status_code, 200)
        # perinfo
        response = self.client.get("/monitor/cpu/perinfo/?cpuNum=0")
        self.assertEqual(response.data, re_cpu[0])
        self.assertEqual(response.status_code, 200)
        # sensor
        response = self.client.get("/monitor/cpu/sensor/")
        self.assertEqual(response.data, re_sen)
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_interrupts.Plugin.update')
    @mock.patch('sysmonitor.plugins.unicorn_load.Plugin')
    def test_readCpuinterr(self, mock_load, mock_interr):
        return_dic = {"min1": 1.0,
                      "min5": 5.4,
                      "min15": 3.3,
                      "cpucore": 4}
        re_interr = {"softirq": 123}
        load = mock.Mock(update=lambda: return_dic)
        mock_load.return_value = load
        mock_interr.return_value = re_interr

        response = self.client.get("/monitor/cpu/interrupts/")

        self.assertEqual(response.data, re_interr)
        self.assertEqual(response.status_code, 200)
