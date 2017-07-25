from django.test import TestCase
import json

# Create your tests here.


class HostListTests(TestCase):
        def test_get(self):
            response = self.client.get("/host/")
            self.assertEqual(response.status_code, 200)

        def test_add_host(self):
            host_dict1 = {"ip": "128.0.0.1", "hostname": "inspur1"}
            host_dict2 = {"ip": "11.1.0.1", "hostname": "inspur2"}
            host_dict3 = {"ip": "11.1.1.1", "hostname": "inspur3"}
            host_dict4 = {"ip": "2323dw322", "hostname": "inspur4"}

            post_data = json.dumps(host_dict1)
            response = self.client.post("/host/", data=post_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 200)

            post_data = json.dumps(host_dict2)
            response = self.client.post("/host/", data=post_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 200)

            post_data = json.dumps(host_dict3)
            response = self.client.post("/host/", data=post_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 200)

            post_data = json.dumps(host_dict4)
            response = self.client.post("/host/", data=post_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 200)

        def test_delete_host(self):
            delete_dict = {"ip": "11.1.11.1"}
            del_dict1 = {"ip": "128.0.0.1"}
            del_dict2 = {"ip": "128.0.0.1,11.1.0.1"}

            delete_data = json.dumps(delete_dict)
            response = self.client.delete("/host/", data=delete_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            elif response.status_code == 500:
                self.assertEqual(response.status_code, 500)
            else:
                self.assertEqual(response.status_code, 200)

            delete_data = json.dumps(del_dict1)
            response = self.client.delete("/host/", data=delete_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            elif response.status_code == 500:
                self.assertEqual(response.status_code, 500)
            else:
                self.assertEqual(response.status_code, 200)

            delete_data = json.dumps(del_dict2)
            response = self.client.delete("/host/", data=delete_data, content_type="application/json")
            if response.status_code == 400:
                self.assertEqual(response.status_code, 400)
            elif response.status_code == 500:
                self.assertEqual(response.status_code, 500)
            else:
                self.assertEqual(response.status_code, 200)
