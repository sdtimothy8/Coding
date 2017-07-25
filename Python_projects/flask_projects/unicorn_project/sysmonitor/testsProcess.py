from django.test import TestCase


# Create your tests here.
class TestProcess(TestCase):
    def test_get_process(self):
        response = self.client.get("/monitor/process/")
        self.assertEqual(response.status_code, 200)

    def test_get_ps_lifecycle(self):
        ps_data = {"pid": "2"}
        response = self.client.get("/monitor/pslifecycle/", data=ps_data)
        self.assertEqual(response.status_code, 200)

    def test_get_ps_io(self):
        ps_data = {"pid": "2"}
        response = self.client.get("/monitor/psio/", data=ps_data)
        self.assertEqual(response.status_code, 200)

    def test_get_ps_files(self):
        ps_data = {"pid": "2"}
        response = self.client.get("/monitor/files/", data=ps_data)
        self.assertEqual(response.status_code, 200)

        ps_data = {"pid": "ddere"}
        response = self.client.get("/monitor/files/", data=ps_data)
        self.assertEqual(response.status_code, 200)

    def test_get_ps_threads(self):
        ps_data = {"pid": "2"}
        response = self.client.get("/monitor/threads/", data=ps_data)
        self.assertEqual(response.status_code, 200)

        ps_data = {"pid": "ddere"}
        response = self.client.get("/monitor/threads/", data=ps_data)
        self.assertEqual(response.status_code, 200)
