"""
The test cases for firewalld features.
Updated by caofengbing@inspur.com.
Added the code using mock.
"""
import json
import mock
from django.test import TestCase


class FirewallListTests(TestCase):

    def test_get_status(self):
        response = self.client.get("/firewall/firewalld/status/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.reload_firewall")
    # @mock.patch("os.system")
    def test_reload(self, mock_reload):
        reload_data = {"complete": "true"}
        put_data = json.dumps(reload_data)
        # mock_cmd.return_value = 0
        mock_reload.return_value = True
        response = self.client.put("/firewall/firewalld/reload/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # mock_cmd.return_value = 1
        mock_reload.return_value = False
        response = self.client.put("/firewall/firewalld/reload/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        reload_data2 = {"complete": "false"}
        put_data = json.dumps(reload_data2)
        # mock_cmd.return_value = 0
        mock_reload.return_value = True
        response = self.client.put("/firewall/firewalld/reload/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # mock_cmd.return_value = 1
        mock_reload.return_value = False
        response = self.client.put("/firewall/firewalld/reload/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_config_type(self):
        data1 = {"config_type": " "}
        # get_data = json.dumps(get_data)
        # mock_cmd.return_value = 0
        response = self.client.get("/firewall/firewalld/config_type/", data=data1)
        self.assertEqual(response.status_code, 200)

        data2 = {"complete": "permanent"}
        response = self.client.get("/firewall/firewalld/config_type/", data=data2)
        self.assertEqual(response.status_code, 200)

        data3 = {"complete": "runtime"}
        response = self.client.get("/firewall/firewalld/config_type/", data=data3)
        self.assertEqual(response.status_code, 200)

    def test_get_panic(self):
        response = self.client.get("/firewall/firewalld/panic/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.set_panic_mode")
    # @mock.patch("os.system")
    def test_put_panic(self, mock_set):
        panic_data = {"panic_mode": "on"}
        put_data = json.dumps(panic_data)
        mock_set.return_value = True
        # mock_cmd.return_value = 0
        response = self.client.put("/firewall/firewalld/panic/", data=put_data, content_type="application/json")
        self.assertTrue(mock_set.called)
        self.assertEqual(response.status_code, 200)
        mock_set.return_value = False
        # mock_cmd.return_value = 1
        response = self.client.put("/firewall/firewalld/panic/", data=put_data, content_type="application/json")
        # self.assertFalse(mock_set.called)
        self.assertEqual(response.status_code, 500)

        panic_data2 = {"panic_mode": "off"}
        put_data = json.dumps(panic_data2)
        # mock_cmd.return_value = 0
        mock_set.return_value = True
        response = self.client.put("/firewall/firewalld/panic/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # mock_cmd.return_value = 1
        mock_set.return_value = False
        response = self.client.put("/firewall/firewalld/panic/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_get_zones(self):
        data1 = {"config_type": " "}
        response = self.client.get("/firewall/firewalld/zones/", data=data1)
        self.assertEqual(response.status_code, 200)

        data2 = {"config_type": "permanent"}
        response = self.client.get("/firewall/firewalld/zones/", data=data2)
        self.assertEqual(response.status_code, 200)

        data3 = {"config_type": "runtime"}
        response = self.client.get("/firewall/firewalld/zones/", data=data3)
        self.assertEqual(response.status_code, 200)

    def test_get_active_zones(self):
        response = self.client.get("/firewall/firewalld/active_zones/")
        self.assertEqual(response.status_code, 200)

    def test_get_default_zone(self):
        response = self.client.get("/firewall/firewalld/default_zone/")
        self.assertEqual(response.status_code, 200)

    # @mock.patch("firewall.business.FirewallManger.get_support_zones")
    @mock.patch("firewall.business.FirewallManger.set_default_zone")
    # @mock.patch("os.system")
    def test_put_default_zone(self, mock_set):
        data1 = {"zone_name": "home"}
        put_data = json.dumps(data1)
        mock_set.return_value = True
        response = self.client.put("/firewall/firewalld/default_zone/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_set.return_value = False
        response = self.client.put("/firewall/firewalld/default_zone/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @mock.patch("firewall.business.FirewallManger.set_default_zone")
    def test_put_default_zone(self, mock_set):
        data2 = {"zone_name": ""}
        put_data = json.dumps(data2)
        mock_set.return_value = False
        response = self.client.put("/firewall/firewalld/default_zone/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @mock.patch("firewall.business.FirewallManger.set_default_zone")
    def test_put_default_zone(self, mock_set):
        data3 = {"zone_name": "dferer"}
        put_data = json.dumps(data3)
        mock_set.return_value = False
        response = self.client.put("/firewall/firewalld/default_zone/", data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_services(self):
        response = self.client.get("/firewall/firewalld/services/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.enable_service")
    # @mock.patch("os.system")
    def test_enable_service(self, mock_enable):
        data1 = {"config_type": "", "zone_name": "", "service_name": "ssh", "time_out": "60"}
        post_data = json.dumps(data1)
        mock_enable.return_value = 'enable success', True
        # mock_cmd.return_value = 0
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_enable.return_value = 'enable success', False
        # mock_cmd.return_value = 1
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data2 = {"config_type": "permanent", "zone_name": "home", "service_name": "ssh"}
        post_data = json.dumps(data2)
        # mock_cmd.return_value = 0
        mock_enable.return_value = 'enable success', True
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # mock_cmd.return_value = 1
        mock_enable.return_value = 'enable success', False
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data3 = {"config_type": "permanent", "zone_name": "", "service_name": "ssh"}
        post_data = json.dumps(data3)

        # mock_cmd.return_value = 0
        mock_enable.return_value = 'enable success', True
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # mock_cmd.return_value = 1
        mock_enable.return_value = 'enable success', False
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data4 = {"config_type": "permanent", "zone_name": "", "service_name": ""}
        post_data = json.dumps(data4)
        # mock_cmd.return_value = 1
        mock_enable.return_value = 'enable success', False
        response = self.client.post("/firewall/firewalld/services/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @mock.patch("firewall.business.FirewallManger.disable_service")
    # @mock.patch("os.system")
    def test_diable_service(self, mock_disable):
        data1 = {"config_type": "", "zone_name": "", "service_name": "ssh"}
        delete_data = json.dumps(data1)
        mock_disable.return_value = 'disable success', True
        # mock_cmd.return_value = 0
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_disable.return_value = 'disable failed ', False
        # mock_cmd.return_value = 1
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data2 = {"config_type": "permanent", "zone_name": "", "service_name": "ssh"}
        delete_data = json.dumps(data2)
        mock_disable.return_value = 'disable success', True
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_disable.return_value = 'disable failed ', False
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data3 = {"config_type": "permanent", "zone_name": "home", "service_name": "ssh"}
        delete_data = json.dumps(data3)
        mock_disable.return_value = 'disable success', True
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_disable.return_value = 'disable failed ', False
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data4 = {"config_type": "", "zone_name": "home", "service_name": "ssh"}
        delete_data = json.dumps(data4)
        mock_disable.return_value = 'disable success', True
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_disable.return_value = 'disable failed ', False
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data5 = {"config_type": "", "zone_name": "home", "service_name": ""}
        delete_data = json.dumps(data5)
        mock_disable.return_value = 'disable failed ', False
        response = self.client.delete("/firewall/firewalld/services/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_enable_services(self):
        data1 = {"config_type": "", "zone_name": "home", "service_name": "ssh"}
        response = self.client.get("/firewall/firewalld/enable_services/", data=data1)
        self.assertEqual(response.status_code, 200)

        data2 = {"config_type": "permanent", "zone_name": "home", "service_name": "ssh"}
        response = self.client.get("/firewall/firewalld/enable_services/", data=data2)
        self.assertEqual(response.status_code, 200)

        data3 = {"config_type": "permanent", "zone_name": "", "service_name": ""}
        response = self.client.get("/firewall/firewalld/enable_services/", data=data3)
        self.assertEqual(response.status_code, 400)

        data4 = {"config_type": "", "zone_name": "home", "service_name": "all"}
        response = self.client.get("/firewall/firewalld/enable_services/", data=data4)
        self.assertEqual(response.status_code, 200)

        data5 = {"config_type": "permanent", "zone_name": "home", "service_name": "all"}
        response = self.client.get("/firewall/firewalld/enable_services/", data=data1)
        self.assertEqual(response.status_code, 200)

    def test_get_ports(self):
        data1 = {"config_type": "", "zone_name": "home"}
        response = self.client.get("/firewall/firewalld/ports/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "", "zone_name": ""}
        response = self.client.get("/firewall/firewalld/ports/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "permanent", "zone_name": ""}
        response = self.client.get("/firewall/firewalld/ports/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "permanent", "zone_name": "home"}
        response = self.client.get("/firewall/firewalld/ports/", data=data1)
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "1", "protocol": "udp"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port success', True
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "1", "protocol": "udp"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port failed', False
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "", "zone_name": "", "ports": "1", "protocol": "udp"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port success', True
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "", "ports": "1", "protocol": "udp"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port success', True
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "", "protocol": "udp"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port failed', False
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "", "protocol": ""}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port failed', False
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_port")
    def test_add_port(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "1", "protocol": ""}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add port failed', False
        response = self.client.post("/firewall/firewalld/ports/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.remove_port")
    def test_delete_port1(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "", "ports": "1", "protocol": "udp"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove port success', True
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_port2(self):
        data1 = {"config_type": "permanent", "zone_name": "", "ports": "", "protocol": "udp"}
        delete_data = json.dumps(data1)
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_port3(self):
        data1 = {"config_type": "permanent", "zone_name": "", "ports": "1", "protocol": ""}
        delete_data = json.dumps(data1)
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @mock.patch("firewall.business.FirewallManger.remove_port")
    def test_delete_port4(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "home", "ports": "1", "protocol": "udp"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove port success', True
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_port")
    def test_delete_port5(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "", "ports": "1", "protocol": "udp"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove port success', True
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_port")
    def test_delete_port6(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "home", "ports": "1", "protocol": "udp"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove port success', True
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_port")
    def test_delete_port7(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "home", "ports": "1", "protocol": "udp"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove port failed', False
        response = self.client.delete("/firewall/firewalld/ports/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_get_interfacess(self):
        data1 = {"config_type": "", "zone_name": "home"}
        response = self.client.get("/firewall/firewalld/interfaces/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "", "zone_name": ""}
        response = self.client.get("/firewall/firewalld/interfaces/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "permanent", "zone_name": ""}
        response = self.client.get("/firewall/firewalld/interfaces/", data=data1)
        self.assertEqual(response.status_code, 200)

        data1 = {"config_type": "permanent", "zone_name": "home"}
        response = self.client.get("/firewall/firewalld/interfaces/", data=data1)
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface1(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "home", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface2(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "home", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface3(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface4(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface5(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface failed', False
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface6(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface7(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface failed', False
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface8(self, mock_delete):
        data1 = {"config_type": "permanent", "zone_name": "home", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface9(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "home", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface10(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "", "interface": "eth0"}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface success', True
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.remove_interface")
    def test_delete_interface11(self, mock_delete):
        data1 = {"config_type": "", "zone_name": "", "interface": ""}
        delete_data = json.dumps(data1)
        mock_delete.return_value = 'remove interface failed', False
        response = self.client.delete("/firewall/firewalld/interfaces/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface1(self, mock_add):
        data1 = {"config_type": "", "zone_name": "", "interface": "eth0"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface success', True
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface2(self, mock_add):
        data1 = {"config_type": "", "zone_name": "", "interface": "eth0"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface failed', False
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface2(self, mock_add):
        data1 = {"config_type": "", "zone_name": "", "interface": ""}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface failed', False
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface3(self, mock_add):
        data1 = {"config_type": "", "zone_name": "home", "interface": "eth0"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface success', True
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface4(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface success', True
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.add_interface")
    def test_add_interface5(self, mock_add):
        data1 = {"config_type": "permanent", "zone_name": "home", "interface": "eth0"}
        add_data = json.dumps(data1)
        mock_add.return_value = 'add interface success', True
        response = self.client.post("/firewall/firewalld/interfaces/", data=add_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface1(self, mock_change):
        data1 = {"config_type": "permanent", "zone_name": "home", "interface": "eth0"}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to success', True
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface2(self, mock_change):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": "eth0"}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to success', True
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface3(self, mock_change):
        data1 = {"config_type": "permanent", "zone_name": "", "interface": ""}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to failed', False
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface4(self, mock_change):
        data1 = {"config_type": "", "zone_name": "", "interface": "eth0"}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to success', True
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface5(self, mock_change):
        data1 = {"config_type": "", "zone_name": "home", "interface": "eth0"}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to success', True
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface6(self, mock_change):
        data1 = {"config_type": "permanent", "zone_name": "home", "interface": ""}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to failed', False
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface7(self, mock_change):
        data1 = {"config_type": "", "zone_name": "home", "interface": ""}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to failed', False
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @mock.patch("firewall.business.FirewallManger.change_interface_zone")
    def test_change_interface8(self, mock_change):
        data1 = {"config_type": "", "zone_name": "", "interface": ""}
        chnage_data = json.dumps(data1)
        mock_change.return_value = 'change the zone an interface belongs to failed', False
        response = self.client.put("/firewall/firewalld/interfaces/", data=chnage_data, content_type="application/json")
        self.assertEqual(response.status_code, 401)
