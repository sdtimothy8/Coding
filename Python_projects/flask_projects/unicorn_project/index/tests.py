from mock import patch
from mock import MagicMock
import subprocess
from django.test import TestCase
import index.views


class TestIndex(TestCase):

    @patch.object(subprocess, 'Popen')
    def test_get(self, subprocess_popen_method):

        comm_retcode = '\nfdsafe:nfieharu'
        output_key = ['HostName', 'System version', 'System kernel', 'Date', 'CPU', 'System running time']
        expected_value = [{'key': item, 'value': comm_retcode.strip()} for item in output_key]
        for item in range(len(expected_value)):
            if expected_value[item]['key'] == 'CPU':
                expected_value[item]['value'] = 'nfieharu'
                break

        subprocess_popen_method.return_value = MagicMock(communicate=lambda: (comm_retcode, 0),
                                                         returncode=0)
        response = index.views.Index().get(None)
        self.assertListEqual(response.data, expected_value)

        # case2
        comm_retcode = 'niopuiareawng:fenwahuhfsbn'
        expected_value = [{'key': item, 'value': comm_retcode} for item in output_key]

        for item in range(len(expected_value)):
            if expected_value[item]['key'] == 'CPU':
                expected_value[item]['value'] = 'fenwahuhfsbn'
                break

        subprocess_popen_method.return_value = MagicMock(communicate=lambda: (comm_retcode, 0),
                                                         returncode=0)
        response = index.views.Index().get(None)

        self.assertListEqual(response.data, expected_value)

        # case3
        expected_value = [{'key': item, 'value': ''} for item in output_key]
        comm_retcode = 'nifaegea'
        subprocess_popen_method.return_value = MagicMock(communicate=lambda: (comm_retcode, 0),
                                                         returncode=1)
        response = index.views.Index().get(None)
        self.assertEquals(response.data, [])
