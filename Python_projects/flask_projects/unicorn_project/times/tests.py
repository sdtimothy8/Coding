import os
import json
from django.test import TestCase
# from users import conststr

# Create your tests here.


class timessTests(TestCase):

    def test_put(self):
        testdict = {"type": "localtime", "time": "Asia/Shanghai"}
        postdata = json.dumps(testdict)
        response = self.client.put("/times/", data=postdata, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        testdict1 = {"type": "sysclock", "time": "2015-7-11 19:24:56"}
        postdata1 = json.dumps(testdict1)
        response1 = self.client.put("/times/", data=postdata1, content_type="application/json")
        self.assertEqual(response1.status_code, 200)

        testdict2 = {"type": "hcclock", "time": "2015-7-11 19:24:56"}
        postdata2 = json.dumps(testdict2)
        response2 = self.client.put("/times/", data=postdata2, content_type="application/json")
        self.assertEqual(response2.status_code, 200)
