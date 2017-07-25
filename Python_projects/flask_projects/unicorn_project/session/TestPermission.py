'''
for permission class test
'''

from mock import MagicMock
from mock import patch
from django.test import TestCase
from Crypto.Cipher import AES
import random
import time
import binascii
from django.conf import settings
import session.permission


class TestPermission(TestCase):
    '''
    test permission class
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(AES, 'new')
    @patch.object(random, 'sample')
    @patch('session.permission.KSMP_Permission.save_to_auth')
    def test_set_permission(self,
                            permission_save_to_auth_method,
                            random_sample_method,
                            aes_new_method):
        # settings = MagicMock(PERMISSION_KEY = '123456',PERMISSION_PREFIX = '1234567890abcdefghijklmnopqrstuvwxyz')
        input_value1 = 'namenamenamenamenamenamenamenamen'

        retcode1 = session.permission.KSMP_Permission().set_permission(input_value1)
        self.assertEquals('', retcode1)

        self.assertFalse(random_sample_method.called)
        self.assertFalse(aes_new_method.called)
        self.assertFalse(permission_save_to_auth_method.called)

        input_value2 = 'zhangsan'
        aes_new_method.return_value = MagicMock(encrypt=lambda text: text)

        random_sample_method.return_value = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        permission_save_to_auth_method.return_value = None

        retcode2 = session.permission.KSMP_Permission().set_permission(input_value2)
        self.assertEquals(retcode2, binascii.b2a_hex('abcdefghizhangsan'))
        self.assertTrue(permission_save_to_auth_method.called)
        self.assertTrue(random_sample_method.called)
        self.assertTrue(permission_save_to_auth_method.called)

    @patch.object(AES, 'new')
    def test_get_permission(self, aes_new_method):
        aes_new_method.return_value = MagicMock(decrypt=lambda text: text)
        input_text1 = '12345fe2a23ce35e'  # length is even
        ret_code1 = session.permission.KSMP_Permission().get_permission(input_text1)
        self.assertEquals(ret_code1, binascii.a2b_hex('12345fe2a23ce35e'))

        input_text2 = '123fe353890a7ce'  # length is odd
        try:
            ret_code2 = session.permission.KSMP_Permission().get_permission(input_text2)
        except TypeError:
            self.fail('should raise error')

        self.assertEquals(None, ret_code2)

        input_text3 = 'feates'  # not hex string
        try:
            ret_code3 = session.permission.KSMP_Permission().get_permission(input_text3)
        except TypeError:
            self.fail('should raise error')

        self.assertEquals(None, ret_code3)

    def test_get_all_auth(self):
        session.permission.KSMP_Permission().set_permission('zhangsan')
        retcode = session.permission.KSMP_Permission().get_all_auth()
        for item in retcode:
            self.assertTrue('zhangsan' in item)

    @patch.object(time, 'time')
    def test_save_to_auth(self, time_time_method):
        time_time_method.return_value = 1234563.378
        input_value1 = 'fhiosteafdas'
        session.permission.KSMP_Permission().save_to_auth(input_value1)
        result = session.permission.KSMP_Permission().get_all_auth()
        self.assertTrue('fhiosteafdas' in result)

    def test_delete_auth(self):
        session.permission.KSMP_Permission().save_to_auth('abcdefghizhangsan')
        retcode1 = session.permission.KSMP_Permission().delete_auth('abcdefghizhangsan')
        self.assertTrue(retcode1)

if __name__ == '__main__':
    testCase = TestPermission()
    testCase.test_set_permission()
