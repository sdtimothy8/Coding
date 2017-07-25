from django.test import TestCase
import os
import json
import mock

__author__ = 'xiek@inspur.com'


class CmdListTest(TestCase):
    """
    test CmdList class
    """

    def test_get(self):

        response = self.client.get("/precmd/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_post(self, mock_cmd):
        testdict1 = {
                    "username": "root",
                    "time": "18:30 2016-7-24",
                    "path": "/",
                    "cmd": "ls"
                    }
        testdict2 = {
                    "username": "kux",
                    "time": "18:30 2016-7-25",
                    "path": "/",
                    "cmd": "ls"
                    }
        testdict3 = {
                    "username": "root",
                    "time": "18:30 2016-9-24",
                    "path": "/tmp",
                    "cmd": "sdgdh"
                    }

        postdata = json.dumps(testdict1)
        mock_cmd.return_value = (0, "success")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

        postdata = json.dumps(testdict2)
        mock_cmd.return_value = (0, "success")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

        postdata = json.dumps(testdict3)
        mock_cmd.return_value = (0, "success")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/precmd/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)


class CmdDetailTest(TestCase):
    def test_get(self):
        response = self.client.get("/precmd/94")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_delete(self, mock_cmd):
        mock_cmd.return_value = (0, "success")
        response = self.client.delete("/precmd/94,95,96")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.delete("/precmd/94,95,96")
        self.assertEqual(response.status_code, 500)
