'''
Test for SessionAuthticateMiddleware and static funcctions
'''
import time
import json
import crypt
from mock import MagicMock
from mock import patch
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from django.conf import settings
import session
import session.permission
import public


class TestSessionAuthticateMiddleWare(TestCase):
    '''
    test for SessionAuthticateMiddleWare
    '''

    def set_up(self):
        pass

    def tear_down(self):
        pass

    @patch('public.functions.unicorn_decrypt')
    @patch('session.SessionAuthticateMiddleWare.isvalid')
    @patch.object(session.permission, 'KSMP_Permission')
    @patch.object(time, 'time')
    def test_process_request(self, time_time_method, ksmp_permission_method, session_auth_isvalid_method, unicorn_method):
        '''
        test for process_request method
        '''

        cookie_value = 'feniaphgergnruaph978y'
        data = '{"username": "yangzg", "password": "yzg.inspur"}'
        permissions = {'feanuigphrisgnnre': 891461.7489,
                       'nuirgehnkhfaruew': 734256.543}
        unicorn_method = MagicMock(lambda test: test)
        request1 = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: cookie_value},
                             GET=MagicMock(copy=lambda: json.loads(data)),
                             POST=json.loads(data),
                             isPermissioned=True,
                             body=data,
                             method='POST')
        time_time_method.return_value = 1234567.890

        ksmp_permission_method.return_value = MagicMock(get_permission=lambda pms: pms if pms in permissions else None,
                                                        get_all_auth=lambda: permissions,
                                                        set_permission=lambda pms: pms
                                                        if pms not in permissions else None,
                                                        save_to_auth=lambda pms, current_time=None: pms
                                                        if pms else pms + ':' + str(current_time),
                                                        delete_auth=lambda pms: pms)
        session_auth_isvalid_method.return_value = True
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request1)

        self.assertTrue(request1.isPermissioned)
        self.assertTrue(ksmp_permission_method.called)
        self.assertTrue(time_time_method.called)
        self.assertTrue(session_auth_isvalid_method.called)

        request1.method = "GET"
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request1)

        self.assertTrue(request1.isPermisssioned)

        # request1.POST = None
        request1.method = "POST"
        self.assertTrue(request1.isPermisssioned)

        session_auth_isvalid_method.return_value = False
        try:
            session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request1)
            self.fail('PermissionDenied should be raise')
        except PermissionDenied:
            pass
        self.assertFalse(request1.isPermissioned)

        data2 = '{"abc":"abc"}'
        request2 = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: cookie_value},
                             GET=MagicMock(copy=lambda: json.loads(data2)),
                             POST=MagicMock(get=lambda _content: data2),
                             isPermissioned=True,
                             body=lambda: data2,
                             method='POST')
        try:
            session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request2)
            self.fail("PermissionDenied should be raise")
        except PermissionDenied:
            pass

        self.assertFalse(request2.isPermissioned)
        request2.method = 'GET'
        try:
            session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request2)
            self.fail("PermissionDenied should be raise")
        except PermissionDenied:
            pass
        self.assertTrue(request2.isPermissioned)

        request2.POST = None
        try:
            session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request2)
            self.fail("PermissionDenied should be raise")
        except PermissionDenied:
            pass
        self.assertTrue(request2.isPermissioned)

        cookie_value2 = 'feanuigphrisgnnre'

        request3 = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: cookie_value2},
                             GET=MagicMock(copy=lambda: data2),
                             POST=MagicMock(get=lambda _content: data2),
                             body=lambda: data2,
                             method='GET',
                             isPermissioned=True)
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request3)
        self.assertTrue(request3.isPermissioned)

        request3.method = 'POST'
        self.assertTrue(request3.isPermissioned)

        request3.POST = None
        self.assertTrue(request3.isPermissioned)

        request4 = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: cookie_value2},
                             GET=MagicMock(copy=lambda: data),
                             POST=MagicMock(get=lambda _content: data),
                             body=lambda: data,
                             method='GET',
                             isPermissioned=True)
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_request(request4)
        self.assertTrue(request4.isPermissioned)

        request4.method = 'POST'
        self.assertTrue(request4.isPermissioned)

        request4.POST = None
        self.assertTrue(request4.isPermissioned)

    def test_process_response(self):
        '''
        test for process_response method
        '''

        cookie_value1 = 'fdafesfni'
        request1 = MagicMock(session=MagicMock(session_key='fnauirheawnfsagiprj',
                                               flush=lambda: 0),
                             COOKIES={settings.SESSION_COOKIE_NAME: cookie_value1})
        data = ['niohiyhe']

        def set_cookie(key=None, value=None, max_age=None,
                       securty=None, expires=None, path=None,
                       domain=None, secure=None, httponly=None):
            data.append('fneihgrsgji')

        response1 = MagicMock(set_cookie=set_cookie)
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_response(request1, response1)
        self.assertEquals(['niohiyhe', 'fneihgrsgji'], data)
        self.assertTrue(request1.COOKIE is not None)

        request2 = MagicMock(session=MagicMock(session_key=None,
                                               flush=lambda: 0),
                             COOKIES={settings.SESSION_COOKIE_NAME: cookie_value1})
        data = ['niohiyhe']
        response2 = MagicMock(set_cookie=set_cookie)
        session.SessionAuthticateMiddleWare.SessionAuthticationMiddleware().process_response(request2, response2)
        self.assertEquals(['niohiyhe'], data)


class TestStaticFunc(TestCase):
    '''
    test for static functions
    '''

    @patch('session.SessionAuthticateMiddleWare.isrootuser')
    @patch('session.SessionAuthticateMiddleWare.isvalidpassword')
    def testisvalid(self, session_isvalidpassword_method, session_isrootuser_method):
        username = 'root'
        password = 'root'
        session_isrootuser_method.return_value = False
        session_isvalidpassword_method.return_value = False
        retcode1 = session.SessionAuthticateMiddleWare.isvalid(username, password)
        self.assertFalse(retcode1)
        self.assertFalse(session_isvalidpassword_method.called)
        self.assertTrue(session_isrootuser_method.called)

        session_isrootuser_method.return_value = True
        session_isvalidpassword_method.return_value = False
        retcode2 = session.SessionAuthticateMiddleWare.isvalid(username, password)
        self.assertFalse(retcode2)
        self.assertTrue(session_isvalidpassword_method.called)

        session_isrootuser_method.return_value = True
        session_isvalidpassword_method.return_value = True
        retcode3 = session.SessionAuthticateMiddleWare.isvalid(username, password)
        self.assertTrue(retcode3)
        self.assertTrue(session_isrootuser_method.called)
        self.assertTrue(session_isvalidpassword_method)

    @patch('__builtin__.open')
    def testisrootuser(self, builtin_open_method):
        '''
        test for isrootuser method
        '''

        index = [-1]
        isclosed = [False]
        file_content = ['zhangsan:h89p243fy4:32',
                        'lisi:renwiqyu89pa:54',
                        'wangwu:rn3uyphf3:35',
                        'maliu:niu9r:930',
                        '']

        def readline():
            index[0] += 1
            return file_content[index[0]]

        def close():
            isclosed[0] = True

        open_file = MagicMock(readline=readline, close=close)
        builtin_open_method.return_value = open_file
        username = ['zhangsan', 'lisi', 'wangwu', 'maliu', 'wuqi', 'zhouba']
        for item in range(len(username)):
            retcode1 = session.SessionAuthticateMiddleWare.isrootuser(username[item])
            self.assertFalse(retcode1)
            self.assertTrue(isclosed[0])
            index = [-1]
            isclosed[0] = False

        file_content = ['zhangsan:h89p243fy4:32',
                        'lisi:renwiqyu89pa:0',
                        'wangwu:rn3uyphf3:35',
                        'maliu: niu9r:930',
                        '']
        index = [-1]
        for item in range(len(username)):
            retcode2 = session.SessionAuthticateMiddleWare.isrootuser(username[item])

            if username[item] == 'lisi':
                self.assertTrue(retcode2)
            else:
                self.assertFalse(retcode2)
            self.assertTrue(isclosed[0])
            index = [-1]
            isclosed[0] = False

        file_content = ['zhangsan:feat4j:234',
                        'lisi:0',
                        'wangwu:fenigt7:9',
                        'masan:3874',
                        '']
        index = [-1]
        for item in range(len(username)):
            retcode3 = session.SessionAuthticateMiddleWare.isrootuser(username[item])
            self.assertFalse(retcode3)
            self.assertTrue(isclosed[0])
            index = [-1]
            isclosed[0] = False

    @patch.object(crypt, 'crypt')
    @patch('__builtin__.open')
    def testisvalidpassword(self, builtin_open_method, crypt_crypt_method):
        '''
        test isvalidpassword method
        '''

        content = ['zhangsan:zhangsan:9999:7',
                   'lisi:$hello$lisi:9999:7',
                   'wangwu:$wangwu$wang$wuwangwu:9999:7',
                   'wuda',
                   'maliu:$wangwu$wang$wuwangwu:feap',
                   '']
        index = [-1]
        flag = [False]

        def readline():
            index[0] += 1
            return content[index[0]]

        def close():
            flag[0] = True

        builtin_open_method.return_value = MagicMock(readline=readline, close=close)
        crypt_crypt_method.return_value = '$wangwu$wang$wuwangwu'
        user_pwd = [{'uname': 'zhangsan', 'pwd': 'zhangsan'},
                    {'uname': 'lisi', 'pwd': 'lisi'},
                    {'uname': 'wangwu', 'pwd': 'wuwangwu'},
                    {'uname': 'wuda', 'pwd': 'wuda'},
                    {'uname': 'maliu', 'pwd': 'maliu'}]
        for item in range(len(user_pwd)):
            retcode = session.SessionAuthticateMiddleWare.isvalidpassword(user_pwd[item]['uname'],
                                                                          user_pwd[item]['pwd'])

            if user_pwd[item]['uname'] == 'wangwu' or user_pwd[item]['uname'] == 'maliu':
                self.assertTrue(retcode)
            else:
                self.assertFalse(retcode)

            self.assertTrue(flag[0])
            index = [-1]
            flag[0] = False
