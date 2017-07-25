import os
import json
from django.test import TestCase
import mock


class packagesTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_post(self, mock_cmd):
        testdict = {
            "path": "/tmp",
            "filename": "webmin-1.700-1.noarch.rpm",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/packages/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/packages/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    @mock.patch("commands.getstatusoutput")
    def test_delete(self, mock_cmd):
        testdict = {
            "forcedel": False,
            "package": "webmin",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.delete("/packages/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.delete("/packages/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
