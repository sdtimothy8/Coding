from django.test import TestCase
import json
import mock

# Create your tests here.


class ServiceTests(TestCase):

    def test_get(self):
        """
        test get service list
        :return:
        """
        response = self.client.get('/service/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('commands.getstatusoutput')
    def test_start_put(self, mock_service):
        """
        test start service
        :param mock_service:
        :return:
        """
        testdata = {
            'services': [{'sname': 'sshd'}],
            'type': 'start'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 0, ''
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 202)

    @mock.patch('commands.getstatusoutput')
    def test_stop_put(self, mock_service):
        """
        test stop service
        :param mock_service:
        :return:
        """
        testdata = {
            'services': [{'sname': 'sshd'}],
            'type': 'stop'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 0, ''
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 202)

    @mock.patch('commands.getstatusoutput')
    def test_restart_put(self, mock_service):
        """
        test restart service
        :param mock_service:
        :return:
        """
        testdata = {
            'services': [{'sname': 'sshd'}],
            'type': 'restart'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 0, ''
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 202)

    @mock.patch('commands.getstatusoutput')
    def test_booton_put(self, mock_service):
        """
        test set the service start with the os
        :param mock_service:
        :return:
        """
        testdata = {
            'services': [{'sname': 'sshd'}],
            'type': 'enable'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 0, ''
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 202)

    @mock.patch('commands.getstatusoutput')
    def test_bootoff_put(self, mock_service):
        """
        test set the service not start with the os
        :param mock_service:
        :return:
        """
        testdata = {
            'services': [{'sname': 'sshd'}],
            'type': 'disable'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 0, ''
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 202)

    @mock.patch('commands.getstatusoutput')
    def test_null_put(self, mock_service):
        """
        test null data
        :param mock_service:
        :return:
        """
        testdata = {}

        putdata = json.dumps(testdata)
        mock_service.return_value = 1
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertFalse(mock_service.called)
        self.assertEqual(response.status_code, 400)

    @mock.patch('commands.getstatusoutput')
    def test_argnull_put(self, mock_service):
        """
        test null arg data
        :param mock_service:
        :return:
        """
        testdata = {
            'services': '',
            'type': 'disable'
        }

        putdata = json.dumps(testdata)
        mock_service.return_value = 1
        response = self.client.put('/service/', data=putdata, content_type='application/json')
        self.assertFalse(mock_service.called)
        self.assertEqual(response.status_code, 400)
