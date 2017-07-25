import json
from django.test import TestCase
import mock

# Create your tests here.


class fansTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "xx|xx|xx|xx|\nFAN|xx|xx|xx")
        response = self.client.get("/fans/fans/all/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (0, "xx|xx|xx|xx|\nFAN|xx|xx|xx")
        response = self.client.get("/fans/fans/1/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/fans/fans/all/")
        self.assertEqual(response.status_code, 500)

        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/fans/fans/1/")
        self.assertEqual(response.status_code, 500)
