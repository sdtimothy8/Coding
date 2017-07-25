'''
for ksmp_session tests
'''

from mock import patch
import time
from django.test import TestCase
import session.permission
from session.ksmp_session import SessionStore


class TestSessionStore(TestCase):
    '''
    test SessionStore class
    '''

    @patch.object(time, 'time')
    def setUp(self, time_time_method):
        '''
        test init
        '''
        time_time_method.return_value = 123456.789
        self.permission = session.permission.KSMP_Permission()
        session_key1 = self.permission.set_permission('zhangsan')
        self.obj1 = SessionStore(session_key=session_key1)
        self.obj2 = SessionStore(session_key='nfidaputiewa')
        self.obj3 = SessionStore()

    def tearDown(self):
        '''
        test finish process
        '''

        session.permission.AuthList = {}
        pass

    @patch('session.ksmp_session.SessionStore.create')
    def test_load(self,  ksmp_session_store_create_method):
        '''
        test load method
        '''

        ret_val = self.obj1.load()
        self.assertFalse(ksmp_session_store_create_method.called)
        self.assertEquals(ret_val, self.permission.get_permission(self.obj1.session_key))

        ksmp_session_store_create_method.called = False
        self.assertFalse(ksmp_session_store_create_method.called)
        ret_val = self.obj2.load()
        self.assertTrue(ksmp_session_store_create_method.called)
        self.assertEquals(ret_val, {})

    def test_exists(self):
        '''
        test exists method
        '''

        ret_value = self.obj1.exists(self.obj1.session_key)
        self.assertTrue(ret_value)

        ret_value = self.obj2.exists('nuirgehnkhfaruew')
        self.assertFalse(ret_value)

    def test_create(self):
        '''
        test create method
        '''

        self.obj1.create()
        self.assertEquals(self.obj1._session_key, None)
        self.assertEquals(self.obj1._session_cache, {})
        self.assertTrue(self.obj1.modified)

    def test_delete(self):
        '''
        test delete method
        '''

        self.assertIsNotNone(self.obj1.session_key)
        self.assertTrue(self.permission.get_permission(self.obj1.session_key) in self.permission.get_all_auth())
        self.obj1.delete(self.obj1.session_key)
        self.assertTrue(self.permission.get_permission(self.obj1.session_key) not in self.permission.get_all_auth())
        self.assertEquals(len(self.permission.get_all_auth()), 0)

        session_key = self.permission.set_permission('lisi')
        case0 = SessionStore(session_key=session_key)
        self.assertTrue(self.permission.get_permission(case0.session_key) in self.permission.get_all_auth())
        case0.delete()
        self.assertTrue(self.permission.get_permission(case0.session_key) not in self.permission.get_all_auth())

        self.permission.set_permission('wangwu')
        self.assertIsNone(self.obj3.session_key)
        self.obj3.delete()
        self.assertEquals(len(self.permission.get_all_auth()), 1)
