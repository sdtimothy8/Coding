from django.test import TestCase
from diskmgr import ifconfig


# Create your tests here.
class DiskmgrTest(TestCase):
    """
    This is the unit test class for disk management.
    Just one thing: queing the disk list and the capacity of each item.
    """
    _module_path = "/diskmgr/capacity/"

    def test_getdisklist(self):
        """
        For function: Get the disk list information.
        1, Check the disk capacity url: /diskmgr/capacity/
        :return:
        """
        cmdstr = self._module_path
        response = self.client.get(cmdstr)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ifconfig.DISK_KEY_LIST)
