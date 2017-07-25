"""
tests for module sysmonitor
"""
from django.test import TestCase
import mock
import json
from sysmonitor.plugins.unicorn_mem_business import MemBusiness
# Create your tests here.


class TestNetworkIOViews(TestCase):

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_throughput_info')
    def test_readThroughput(self, mock_throughput):
        return_update = True, []
        mock_throughput.return_value = return_update
        response = self.client.get("/monitor/throughput/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_throughput_info')
    def test_readThroughput(self, mock_throughput):
        return_update = False, []
        mock_throughput.return_value = return_update
        response = self.client.get("/monitor/throughput/")
        self.assertEqual(response.data, {'result': {'message': 'error', 'type': 'error'}})
        self.assertEqual(response.status_code, 500)\


    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_socket_info')
    def test_readThroughput(self, mock_socket):
        return_update = True, []
        mock_socket.return_value = return_update
        response = self.client.get("/monitor/socket/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_socket_info')
    def test_readThroughput(self, mock_socket):
        return_update = False, []
        mock_socket.return_value = return_update
        response = self.client.get("/monitor/socket/")
        self.assertEqual(response.data, {'result': {'message': 'error', 'type': 'error'}})
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_iptrafic_info')
    def test_readThroughput(self, mock_iptrafic):
        return_update = True, []
        mock_iptrafic.return_value = return_update
        response = self.client.get("/monitor/iptrafic/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_iptrafic_info')
    def test_readThroughput(self, mock_iptrafic):
        return_update = False, []
        mock_iptrafic.return_value = return_update
        response = self.client.get("/monitor/iptrafic/")
        self.assertEqual(response.data, {'result': {'message': 'error', 'type': 'error'}})
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_udp_info')
    def test_readThroughput(self, mock_udp):
        return_update = True, []
        mock_udp.return_value = return_update
        response = self.client.get("/monitor/udp/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_udp_info')
    def test_readThroughput(self, mock_udp):
        return_update = False, []
        mock_udp.return_value = return_update
        response = self.client.get("/monitor/udp/")
        self.assertEqual(response.data, {'result': {'message': 'error', 'type': 'error'}})
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_tcp_info')
    def test_readThroughput(self, mock_tcp):
        return_update = True, []
        mock_tcp.return_value = return_update
        response = self.client.get("/monitor/tcp/")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    @mock.patch('sysmonitor.plugins.unicorn_network_io.NetworkIO.get_tcp_info')
    def test_readThroughput(self, mock_tcp):
        return_update = False, []
        mock_tcp.return_value = return_update
        response = self.client.get("/monitor/tcp/")
        self.assertEqual(response.data, {'result': {'message': 'error', 'type': 'error'}})
        self.assertEqual(response.status_code, 500)


class TestMemCase(TestCase):

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.MemBusiness.get_mem_info')
    def test_getmem(self, mock_getmeminfo):
        """
        test the GET method
        :param mock_getmeminfo:
        :return:
        """

        mock_getmeminfo.return_value = True, {}

        response = self.client.get("/monitor/mem/")
        self.assertEqual(response.data, {'meminfo': {}})
        self.assertEqual(response.status_code, 200)

        mock_getmeminfo.return_value = False, {}

        response = self.client.get("/monitor/mem/")
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.MemBusiness.get_swap_info')
    def test_getswap(self, mock_getswapinfo):
        """
        test the GET method
        :param mock_getswapinfo:
        :return:
        """
        test_data = {
            "keys": "all"
        }
        post_data = json.dumps(test_data)

        mock_getswapinfo.return_value = True, {}

        response = self.client.get("/monitor/swap/")
        self.assertEqual(response.data, {'swapinfo': {}})
        self.assertEqual(response.status_code, 200)

        mock_getswapinfo.return_value = False, {}

        response = self.client.get("/monitor/swap/")
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.MemBusiness.get_page_info')
    def test_getpage(self, mock_getpageinfo):
        """
        test the GET method
        :param mock_getpageinfo:
        :return:
        """
        test_data = {
            "keys": "all"
        }
        post_data = json.dumps(test_data)

        mock_getpageinfo.return_value = True, {}

        response = self.client.get("/monitor/page/")
        self.assertEqual(response.data, {'pageinfo': {}})
        self.assertEqual(response.status_code, 200)

        mock_getpageinfo.return_value = False, {}

        response = self.client.get("/monitor/page/")
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.MemBusiness.get_slab_info')
    def test_getslab(self, mock_getslabinfo):
        """
        test the GET method
        :param mock_getslabinfo:
        :return:
        """
        test_data = {
            "keys": "all"
        }
        post_data = json.dumps(test_data)

        mock_getslabinfo.return_value = True, {}

        response = self.client.get("/monitor/slab/")
        self.assertEqual(response.data, {'slabinfo': {}})
        self.assertEqual(response.status_code, 200)

        mock_getslabinfo.return_value = False, {}

        response = self.client.get("/monitor/slab/")
        self.assertEqual(response.status_code, 500)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.MemBusiness.get_numastat_info')
    def test_getnumastat(self, mock_getnumastatinfo):
        """
        test the GET method
        :param mock_getnumastatinfo:
        :return:
        """
        test_data = {
            "keys": "all"
        }
        post_data = json.dumps(test_data)

        mock_getnumastatinfo.return_value = True, {}

        response = self.client.get("/monitor/numastat/")
        self.assertEqual(response.data, {'numastat': {}})
        self.assertEqual(response.status_code, 200)

        mock_getnumastatinfo.return_value = False, {}

        response = self.client.get("/monitor/numastat/")
        self.assertEqual(response.status_code, 500)

    @mock.patch('psutil.virtual_memory')
    @mock.patch('sysmonitor.plugins.unicorn_mem_business.functions.launchcmd')
    def test_business_getmem(self, mock_launchcmd, mock_mem):
        """
        :return:
        """
        mem_data = "svmem(total=1768493056L, available=499630080L, percent=71.7, used=1653415936L, free=115077120L, " \
                   "active=1091244032, inactive=379768832, buffers=0L, cached=384552960)"

        all_data = {
                        "available": "499630080L",
                        "used": "1653415936L",
                        "cached": "384552960",
                        "percent": "71.7",
                        "free": "115077120L",
                        "inactive": "379768832",
                        "active": "1091244032",
                        "total": "1768493056L",
                        "buffers": "0L",
                        "shared": 326107136
                    }

        one_data = {"free": "115077120L"}

        file_object = open('monitor_test_temp0', 'w')
        file_object.write("              total        used        free      shared  buff/cache   available\n"
                          "Mem:        1727044     1057068      102856      318464      567120      126936\n"
                          "Swap:       3932156        5292     3926864")
        file_object.close()
        mock_launchcmd.return_value = open("monitor_test_temp0", 'r')

        mock_mem.return_value = mem_data

        rtn_flag, rtn_date = MemBusiness.get_mem_info(["all"])
        
        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, all_data)

        rtn_flag, rtn_date = MemBusiness.get_mem_info(["free"])

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, one_data)

    @mock.patch('psutil.swap_memory')
    @mock.patch('sysmonitor.plugins.unicorn_mem_business.functions.launchcmd')
    def test_business_getswap(self, mock_launchcmd, mock_swap):
        """
        :return:
        """
        swap_data = "sswap(total=4026527744L, used=574189568L, free=3452338176L, " \
                    "percent=14.3, sin=508444672, sout=847052800)"

        file_object = open('monitor_test_temp', 'w')
        file_object.write("Linux 3.10.0-229.el7.x86_64 (localhost.localdomain) 	12/10/2015 	_x86_64_	(2 CPU)\n"
                          " 09:12:01 AM  pswpin/s pswpout/s \n 09:12:02 AM      0.00      0.00 \n "
                          "Average:         0.00      0.00")
        file_object.close()
        mock_launchcmd.return_value = open("monitor_test_temp", 'r')

        all_data = {
                        "pswpout": "0.00",
                        "total": "4026527744L",
                        "free": "3452338176L",
                        "used": "574189568L",
                        "pswpin": "0.00"
                    }

        one_data = {"free": "3452338176L"}

        mock_swap.return_value = swap_data

        rtn_flag, rtn_date = MemBusiness.get_swap_info(["all"])

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, all_data)

        rtn_flag, rtn_date = MemBusiness.get_swap_info(["free"])

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, one_data)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.functions.launchcmd')
    def test_business_getslab(self, mock_launchcmd):
        """
        :return:
        """

        file_object = open('monitor_test_temp2', 'w')
        file_object.write(" Active / Total Objects (% used)    : 277392 / 325769 (85.1%) \n"
                          "Active / Total Slabs (% used)      : 11512 / 11512 (100.0%) \n"
                          "Active / Total Caches (% used)     : 69 / 95 (72.6%) \n"
                          "Active / Total Size (% used)       : 65222.95K / 77949.13K (83.7%) \n"
                          "Minimum / Average / Maximum Object : 0.01K / 0.24K / 15.88K \n"
                          " \n"
                          "OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ/SLAB CACHE SIZE NAME \n                  "
                          "79296  53512  67%    0.06K   1239       64      4956K kmalloc-64  \n          "
                          " 31458  29662  94%    0.19K   1498       21      5992K dentry   \n            "
                          "  30276  30026  99%    0.21K   1682       18      6728K vm_area_struct         ")
        file_object.close()
        mock_launchcmd.return_value = open("monitor_test_temp2", 'r')

        all_data = [{
            "objs": "79296",
            "name": "kmalloc-64",
            "obj_slab": "64",
            "use": "67%",
            "active": "53512",
            "obj_size": "0.06K",
            "slabs": "1239"
        }, {
            "objs": "31458",
            "name": "dentry",
            "obj_slab": "21",
            "use": "94%",
            "active": "29662",
            "obj_size": "0.19K",
            "slabs": "1498"
        }, {
            "objs": "30276",
            "name": "vm_area_struct",
            "obj_slab": "18",
            "use": "99%",
            "active": "30026",
            "obj_size": "0.21K",
            "slabs": "1682"
        }]

        one_data = {"use": "99%"}

        rtn_flag, rtn_date = MemBusiness.get_slab_info("", ["all"])

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, all_data)

        mock_launchcmd.return_value = open("monitor_test_temp2", 'r')
        rtn_flag, rtn_date = MemBusiness.get_slab_info("vm_area_struct", ["use"])

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, one_data)

    @mock.patch('sysmonitor.plugins.unicorn_mem_business.functions.launchcmd')
    def test_business_getnumastat(self, mock_launchcmd):
        """
        :return:
        """

        file_object = open('monitor_test_temp3', 'w')
        file_object.write("                           node0  node1  node2 \n"
                          "numa_hit                45456046    21     2 \n"
                          "numa_miss                      0    23        4 \n"
                          "numa_foreign                   0    32        3 \n"
                          "interleave_hit               522    12       1 \n"
                          "local_node              45456046   23            5 \n"
                          "other_node                     0    35            8 \n")
        file_object.close()
        mock_launchcmd.return_value = open("monitor_test_temp3", 'r')

        all_data = [
                        {
                            "local_node": "45456046",
                            "name": "node0",
                            "other_node": "0",
                            "numa_miss": "0",
                            "interleave_hit": "522",
                            "numa_foreign": "0",
                            "numa_hit": "45456046"
                        },
                        {
                            "local_node": "23",
                            "name": "node1",
                            "other_node": "35",
                            "numa_miss": "23",
                            "interleave_hit": "12",
                            "numa_foreign": "32",
                            "numa_hit": "21"
                        },
                        {
                            "local_node": "5",
                            "name": "node2",
                            "other_node": "8",
                            "numa_miss": "4",
                            "interleave_hit": "1",
                            "numa_foreign": "3",
                            "numa_hit": "2"
                        }
                    ]

        rtn_flag, rtn_date = MemBusiness.get_numastat_info()

        self.assertEqual(rtn_flag, True)
        self.assertEqual(rtn_date, all_data)
