import json
from django.test import TestCase
import mock

# Create your tests here.


class userTests(TestCase):

    def test_get(self):
        response = self.client.get("/user/")
        self.assertEqual(response.status_code, 200)

    def test_userinfo(self):
        response = self.client.get("/user/root/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_post(self, mock_cmd):
        testdict = {
            "uname": "test1",
            "fullname": "test user",
            "password": "qwe123567",
            "shell": "/sbin/",
            "homedir": "/home/test1/",
            "uid": "",
            "gid": ""
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    @mock.patch("commands.getstatusoutput")
    def test_post1(self, mock_cmd):
        testdict = {
            "uname": "user1",
            "fullname": "user1",
            "password": "23567",
            "shell": "/sbin/",
            "homedir": "",
            "uid": "",
            "gid": ""
            }

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        mock_cmd.return_value = (1, "failed")
        response = self.client.post("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    @mock.patch("commands.getstatusoutput")
    def test_put(self, mock_cmd):
        testdict = {
            'uname': 'test1',
            'newname': 'newuser',
            'fullname': 'just for test',
            'password': 'qwe123567',
            'shell': '/sbin/',
            'homedir': '/home/newuser/'
            }
        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.put("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 202)
        mock_cmd.return_value = (1, "failed")
        response = self.client.put("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 500)

    @mock.patch("commands.getstatusoutput")
    def test_delete(self, mock_cmd):
        testdict = {'users': [{'uname': 'user1'}]}
        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.delete("/user/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)


class groupTests(TestCase):

    def test_get(self):
        response = self.client.get("/group/")
        self.assertEqual(response.status_code, 200)

    def test_group_users(self):
        response = self.client.get("/group/root/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("commands.getstatusoutput")
    def test_post(self, mock_cmd):
        testdict = {"gname": "testgroup", "gid": "1111"}

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/group/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    # gid is null
    @mock.patch("commands.getstatusoutput")
    def test_post1(self, mock_cmd):
        testdict = {"gname": "testgroup", "gid": ""}

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.post("/group/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    @mock.patch("commands.getstatusoutput")
    def test_addtogroup(self, mock_cmd):
        testdict = {"type": "add", "groups": [{"gname": "testgroup", "uname": "test1"}]}

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.put("/group/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 202)

    @mock.patch("commands.getstatusoutput")
    def test_deletefromgroup(self, mock_cmd):
        testdict = {"type": "delete", "groups": [{"gname": "testgroup", "uname": "test1"}]}

        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.put("/group/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 202)

    @mock.patch("commands.getstatusoutput")
    def test_delete(self, mock_cmd):
        testdict = {'groups': [{'gname': 'testgroup'}, {'gname': 'test_group'}]}
        postdata = json.dumps(testdict)
        mock_cmd.return_value = (0, "sucess")
        response = self.client.delete("/group/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)
