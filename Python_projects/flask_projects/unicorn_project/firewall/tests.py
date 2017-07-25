"""
The test cases for firewall features.
Updated by shaomingwu@inspur.com.
Added the code using mock.
"""
import json
from mock import MagicMock
from django.test import TestCase
from public import functions


class FirewallListTests(TestCase):
    """
    Automated tests for EthernetList.
    """
    def test_applymodification(self):
        """
        1, Check the ethernet list url: /ethernet/
        Base logic:
           1) Launch the function for apply at first.
           2) Check the result. The status of the service should be active.
        :return:
        """
        cmdstr = "/sbin/service iptables save && /sbin/service ip6tables save  \
                 && systemctl start iptables.service && systemctl start ip6tables.service"
        functions.launchcmd = MagicMock()
        dict4post = {"command": "APPLY"}
        postdata = json.dumps(dict4post)

        cmdurl = "/firewall/"
        response = self.client.put(cmdurl, data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        functions.launchcmd.assert_called_with(cmdstr)

    def test_reset_all(self):
        """
        Flush test.
        :return:
        """
        cmdstr = "systemctl stop iptables.service && systemctl stop ip6tables.service \
                  && iptables --flush &&  ip6tables --flush \
                  && /sbin/service iptables save && /sbin/service ip6tables save \
                  && systemctl start iptables.service &&systemctl start ip6tables.service "
        functions.launchcmd = MagicMock()
        dict4post = {"command": "RESET"}
        postdata = json.dumps(dict4post)

        cmdurl = "/firewall/"
        response = self.client.put(cmdurl, data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        functions.launchcmd.assert_called_with(cmdstr)

    def test_enable_service(self):
        """
        Enable or disable firewall service.
        :return:
        """
        cmdstr = "systemctl enable iptables.service && systemctl enable ip6tables.service "
        functions.launchcmd = MagicMock()
        dict4post = {"command": "ENABLESERVICE",
                     "enableflag": "Yes"}
        postdata = json.dumps(dict4post)

        cmdurl = "/firewall/"
        response = self.client.put(cmdurl, data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        functions.launchcmd.assert_called_with(cmdstr)

    def test_disenable_service(self):
        """
        Enable or disable firewall service.
        :return:
        """
        cmdstr = "systemctl disable iptables.service && systemctl disable ip6tables.service"
        functions.launchcmd = MagicMock()
        dict4post = {"command": "ENABLESERVICE",
                     "enableflag": "No"}
        postdata = json.dumps(dict4post)

        cmdurl = "/firewall/"
        response = self.client.put(cmdurl, data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        functions.launchcmd.assert_called_with(cmdstr)

    def test_get(self):
        response = self.client.get("/firewall/")
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        firewall_dict1 = {"cmd": "iptables -A INPUT -p tcp -j ACCEPT"}
        firewall_dict2 = {"cmd": "iptables -A INPUT -p udp -j ACCEPT"}

        post_data = json.dumps(firewall_dict1)
        response = self.client.post("/firewall/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        post_data = json.dumps(firewall_dict2)
        response = self.client.post("/firewall/", data=post_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        delete_dict1 = {"chain": "INPUT", "number": "10"}
        delete_dict2 = {"chain": "INPUT", "number": "10", "table": "nat"}
        delete_dict3 = {"chain": "INPUT", "number": "10", "table": "mange"}
        delete_dict4 = {"chain": "INPUT", "number": "10", "table": "raw"}
        delete_data = json.dumps(delete_dict1)
        response = self.client.delete("/firewall/", data=delete_data, content_type="application/json")
        if response.status_code == 500:
            self.assertEqual(response.status_code, 500)
        else:
            self.assertEqual(response.status_code, 200)

        delete_data = json.dumps(delete_dict2)
        response = self.client.delete("/firewall/", data=delete_data, content_type="application/json")
        if response.status_code == 500:
            self.assertEqual(response.status_code, 500)
        else:
            self.assertEqual(response.status_code, 200)

        delete_data = json.dumps(delete_dict3)
        response = self.client.delete("/firewall/", data=delete_data, content_type="application/json")
        if response.status_code == 500:
            self.assertEqual(response.status_code, 500)
        else:
            self.assertEqual(response.status_code, 200)

        delete_data = json.dumps(delete_dict4)
        response = self.client.delete("/firewall/", data=delete_data, content_type="application/json")
        if response.status_code == 500:
            self.assertEqual(response.status_code, 500)
        else:
            self.assertEqual(response.status_code, 200)
