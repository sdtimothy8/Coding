import json
from django.test import TestCase
import mock

# Create your tests here.


class fdisklistTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx|xx|xx|xx|\nFAN|xx|xx|xx")
        response = self.client.get("/driver/disk/getfdiskdriver/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/disk/getfdiskdriver/")
        self.assertEqual(response.status_code, 500)

        mock_cmd.return_value = (0, "devtmpfs                 5.8G     0  5.8G    0% /dev\ndevtmpfs                 5.8G     0  5.8G    0% /dev")
        response = self.client.get("/driver/disk/getfdisklist/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/disk/getfdisklist/")
        self.assertEqual(response.status_code, 500)


class networklistTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx|xx|xx|xx|\nFAN|xx|xx|xx")
        response = self.client.get("/driver/network/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/network/")
        self.assertEqual(response.status_code, 500)


class pcilistTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx|xx|xx|xx|\nFAN|xx|xx|xx")
        response = self.client.get("/driver/pci/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/pci/")
        self.assertEqual(response.status_code, 500)


class drivermodslistTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx xx xx xx xx\nxx xx xx")
        response = self.client.get("/driver/drivermodslist/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/drivermodslist/")
        self.assertEqual(response.status_code, 500)


class drivermodinfoTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx xx xx xx xx\nxx xx xx")
        response = self.client.get("/driver/drivermodinfo/ptp/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "")
        response = self.client.get("/driver/drivermodinfo/pt/")
        self.assertEqual(response.status_code, 500)
