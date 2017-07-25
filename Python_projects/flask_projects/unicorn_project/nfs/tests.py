import json
from django.test import TestCase
import mock

# Create your tests here.


class checkdirTests(TestCase):

    @mock.patch("os.path.exists")
    def test_post(self, mock_cmd):
        testdict = {
            'path': "/error"
            }

        mock_cmd.return_value = (0, "sucess")
        postdata = json.dumps(testdict)
        response = self.client.post("/nfs/dir/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class checkuidTests(TestCase):

    def test_post(self):
        testdict = {
            'anonuid': "501"
            }

        postdata = json.dumps(testdict)
        response = self.client.post("/nfs/uid/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class checkgidTests(TestCase):

    def test_post(self):
        testdict = {
            'anongid': "501"
            }

        postdata = json.dumps(testdict)
        response = self.client.post("/nfs/gid/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class checknfsTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "sucess")
        response = self.client.get("/nfs/checknfs/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/nfs/checknfs/")
        self.assertEqual(response.status_code, 500)


class nfsTests(TestCase):

    @mock.patch("commands.getstatusoutput")
    def test_get(self, mock_cmd):
        mock_cmd.return_value = (0, "sucess")
        response = self.client.get("/nfs/")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.get("/nfs/")
        self.assertEqual(response.status_code, 500)

    @mock.patch("commands.getstatusoutput")
    def test_post(self, mock_cmd):
        testdict = {
            "cmd": "add",
            "line": "test cmd",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

        testdict = {
            "cmd": "del",
            "line": "test cmd",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

        testdict = {
            "cmd": "on",
            "line": "#test cmd",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

        testdict = {
            "cmd": "off",
            "line": "test cmd",
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/nfs/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)
