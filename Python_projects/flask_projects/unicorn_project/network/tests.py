from django.test import TestCase
import json
from mock import patch, Mock, MagicMock


class TestDeviceList(TestCase):
    """
    Unit test for getting network device information
    """
    def test_get(self):
        """
        Test for getting network device info
        """
        response = self.client.get("/network/")
        self.assertEqual(response.status_code, 200)

    @patch('NetworkManager.NetworkManager.GetDeviceByIpIface')
    @patch('commands.getstatusoutput')
    @patch('NetworkManager.Settings.GetConnectionByUuid')
    @patch('NetworkManager.NetworkManager.ActivateConnection')
    @patch('NetworkManager.NetworkManager.DeactivateConnection')
    def test_post(self,
                  deactivate_connection,
                  activate_connection,
                  get_connection,
                  get_status_output,
                  get_device):
        """
        Test for changing network device/connection state
        """
        # case 1
        test_dict1 = {
                'DevName': 'enp2s0',
                'Action': 'activate',
                'Label': 'device'}
        post_data = json.dumps(test_dict1)
        get_device.return_value = 'dev'
        get_connection.return_value = 'connection'

        get_status_output.return_value = (0, 'success')
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        get_status_output.return_value = (-1, 'failed')
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        # case 2
        test_dict2 = {
                'DevName': 'enp2s0',
                'Action': 'deactivate',
                'Label': 'device'}
        post_data = json.dumps(test_dict2)
        get_status_output.return_value = (0, 'success')
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        get_status_output.return_value = (-1, 'failed')
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 500)
        # case 3
        test_dict3 = {
            'DevName': 'enp2s0',
            'Uuid': 'ac5fbcd5-e2f9-4f32-a5f9-af9d71a81f93',
            'Action': 'activate',
            'Label': 'connection'}
        post_data = json.dumps(test_dict3)
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertTrue(activate_connection.called)
        self.assertEqual(response.status_code, 200)
        # case 4
        test_dict4 = {
            'DevName': 'enp2s0',
            'Uuid': 'ac5fbcd5-e2f9-4f32-a5f9-af9d71a81f93',
            'Action': 'deactivate',
            'Label': 'connection'}
        post_data = json.dumps(test_dict4)
        response = self.client.post("/network/", data=post_data, content_type="application/json")
        self.assertTrue(deactivate_connection.called)
        self.assertEqual(response.status_code, 200)

    @patch('NetworkManager.Settings.GetConnectionByUuid')
    def test_delete(self, get_connection):
        """
        Test for delete a connection
        """
        conn = MagicMock(Delete=lambda: 'delete')
        test_dict1 = {"Uuid": "ac5fbcd5-e2f9-4f32-a5f9-af9d71a81f93"}
        post_data = json.dumps(test_dict1)
        get_connection.return_value = conn
        response = self.client.delete("/network/", data=post_data, content_type="application/json")
        # self.assertTrue(delete_connection.called)
        self.assertEqual(response.status_code, 200)


class TestAddConnection(TestCase):
    """
    Unit test for adding a connection
    """
    def test_get(self):
        """
        Test for get mac address list
        """
        response = self.client.get("/network/add_conn/")
        self.assertEqual(response.status_code, 200)

    @patch('NetworkManager.Settings.AddConnection')
    def test_post(self, add_connection):
        """
        Test for add a connection
        """
        # case 1:manual method
        test_dict1 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict1)
        response = self.client.post("/network/add_conn/", data=post_data, content_type="application/json")
        self.assertTrue(add_connection.called)
        self.assertEqual(response.status_code, 200)

        # case 2:auto method
        test_dict2 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'dns': ['192.168.137.1'],
                'method': 'auto',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'auto',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict2)
        response = self.client.post("/network/add_conn/", data=post_data, content_type="application/json")
        self.assertTrue(add_connection.called)
        self.assertEqual(response.status_code, 200)

        # case 3:Invalid clone mac address
        test_dict3 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': 'C0:7C:D1:3D:17',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict3)
        response = self.client.post("/network/add_conn/", data=post_data, content_type="application/json")
        self.assertTrue(add_connection.called)
        self.assertEqual(response.status_code, 500)

        # case 4:Invalid ipv4 address
        test_dict4 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict4)
        response = self.client.post("/network/add_conn/", data=post_data, content_type="application/json")
        self.assertTrue(add_connection.called)
        self.assertEqual(response.status_code, 500)

        # case 5:Invalid ipv6 address
        test_dict5 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.93', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1x']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict5)
        response = self.client.post("/network/add_conn/", data=post_data, content_type="application/json")
        self.assertTrue(add_connection.called)
        self.assertEqual(response.status_code, 500)


class TestConnectionDetail(TestCase):
    """
    Unit test for modifying a connection configure information
    """
    @patch('NetworkManager.Settings.GetConnectionByUuid')
    def test_get(self, get_connection):
        """
        Test for getting mac address list
        """
        conn = MagicMock(GetSettings=lambda: {'802-3-ethernet': {}, 'connection': {}, 'ipv4': {}, 'ipv6': {}})
        get_connection.return_value = conn
        response = self.client.get("/network/12345678-1234-1234-1234-123456789abc/")
        self.assertEqual(response.status_code, 200)

    @patch('NetworkManager.Settings.GetConnectionByUuid')
    def test_post(self, get_connection):
        """
        Test for resetting connection configure
        """
        conn = MagicMock(GetSettings=lambda: {'802-3-ethernet': {}, 'connection': {}, 'ipv4': {}, 'ipv6': {}},
                         Update=lambda x: 'update')
        get_connection.return_value = conn
        test_dict1 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {},
            'IPv6': {}
        }
        post_data = json.dumps(test_dict1)
        response = self.client.post("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @patch('NetworkManager.Settings.GetConnectionByUuid')
    def test_put(self, get_connection):
        """
        Test for updating connection configure
        """
        conn = MagicMock(Update=lambda x: 'update')
        get_connection.return_value = conn
        # case 1
        test_dict1 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:74',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'dns': ['192.168.137.1'],
                'method': 'auto',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'dns': [],
                'method': 'auto',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict1)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # case 2
        test_dict2 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': 'C0:7C:D1:3D:17:23',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict2)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # case 3:Invalid clone mac address
        test_dict3 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': 'C0:7C:D1:3D:17',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict3)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 500)

        # case 4:Invalid ipv4 address
        test_dict4 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': '',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict4)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 500)

        # case 5:Invalid ipv6 address
        test_dict5 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': 'C0:7C:D1:3D:17',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137.1'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'dns': ['fe80::c27c:d1ff:fe3d:1'],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict5)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 500)

        # case 6:empty ipv4/ipv6 address when method is manual
        test_dict6 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [],
                'dns': ['192.168.137.1'],
                'method': 'manual',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [],
                'method': 'manual',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict6)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 500)

        # case 7:link-local method
        test_dict7 = {
            'Identity': {
                'name': 'ethx',
                'mac-address': 'C0:7C:D1:3D:17:23',
                'cloned-mac-address': '',
                'mtu': 0,
                'autoconnect': True,
                'permissions': True
            },
            'IPv4': {
                'addresses': [['192.168.137.92', 24, '192.168.137'], ['192.168.137.92', 24, '192.168.137.2']],
                'dns': ['192.168.137.1'],
                'method': 'link-local',
                'ignore-auto-dns': False,
                'never-default': False
            },
            'IPv6': {
                'addresses': [['fe80::c27c:d1ff:fe3d:1774', 64, 'fe80::c27c:d1ff:fe3d:1']],
                'method': 'link-local',
                'ignore-auto-dns': True,
                'never-default': True
            },
        }
        post_data = json.dumps(test_dict7)
        response = self.client.put("/network/12345678-1234-1234-1234-123456789abc/", data=post_data,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
