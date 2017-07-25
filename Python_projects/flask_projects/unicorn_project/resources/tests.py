from django.test import TestCase
import json
import mock
# Create your tests here.


class ResourcesListTests(TestCase):
    """
    test get resource info
    """
    def test_get_ps(self):
        """
        test get ps info
        :return:
        """
        response = self.client.get("/resources/ps/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("os.system")
    def test_delete_ps(self, mock_cmd):
        """
        test delete ps info
        :param mock_cmd:
        :return:
        """
        delete_dict = {"pid": "2005"}
        delete_data = json.dumps(delete_dict)
        mock_cmd.return_value = 0
        response = self.client.delete("/resources/psdetail/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        mock_cmd.return_value = 1
        response = self.client.delete("/resources/psdetail/", data=delete_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)


class Test_GetReources(TestCase):
    """
    test get Reourcese info
    """

    def test_get_ps(self):
        """
        test get ps info
        :return:
        """
        response = self.client.get("/resources/")
        self.assertEqual(response.status_code, 200)

    def test_get_cpumem(self):
        """
        test get cpu and memory info
        :return:
        """
        response = self.client.get("/resources/pscpumem/")
        self.assertEqual(response.status_code, 200)

    def test_get_netinfo(self):
        """
        test get network io info
        :return:
        """
        response = self.client.get("/resources/psnetinfo/")
        self.assertEqual(response.status_code, 200)

    def test_get_diskinfo(self):
        """
        test get disk io info
        :return:
        """
        response = self.client.get("/resources/psdiskinfo/")
        self.assertEqual(response.status_code, 200)


class Test_PciList(TestCase):
    """
    test get pci info
    """

    def test_get_pci(self):
        """
        test get pci info
        :return:
        """
        response = self.client.get("/resources/pci/")
        self.assertEqual(response.status_code, 200)


class Test_UsbList(TestCase):
    """
    test get usb info
    """

    def test_get_usb(self):
        """
        test get usb info
        :return:
        """
        response = self.client.get("/resources/usb/")
        self.assertEqual(response.status_code, 200)
