from mock import patch
from mock import MagicMock
from django.test import TestCase
from django.conf import settings
from rest_framework import status
from session.permission import KSMP_Permission
import session.permission
import login.views
from public import functions


class TestLoginViews(TestCase):
    '''
    for login view test
    '''

    def test_get(self):
        '''
        test get method
        '''

        request = MagicMock(isPermissioned=True)
        response = login.views.Login().get(request)
        self.assertDictEqual(response.data[0], {"status": "success",
                                                "message": "login success"})

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        request = MagicMock(isPermissioned=False)
        response = login.views.Login().get(request)

        self.assertDictEqual(response.data[0], {"status": "fail",
                                                "message": "login fail"})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @patch.object(functions, 'unicorn_decrypt')
    @patch('session.SessionAuthticateMiddleWare.isvalid')
    def test_post(self, middleware_isvalid_method, functions_unicorn_decrypt_method):
        '''
        test post method
        '''

        # first case
        request = MagicMock(data={'username': 'zhangsan', 'password': 'zhs'},
                            isPermissioned=True)
        middleware_isvalid_method.return_value = True

        response = login.views.Login().post(request)

        self.assertDictEqual(response.data[0], {"status": "success",
                                                "message": "login success"})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # second case
        request = MagicMock(data={'abc': 'abc'}, isPermissioned=True)
        response = login.views.Login().post(request)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # third case
        request = MagicMock(data={'username': 'zhangsan', 'password': 'zhs'},
                            isPermissioned=False)
        response = login.views.Login().post(request)
        self.assertDictEqual(response.data[0], {"status": "fail",
                                                'message': 'login fail'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # fouth case
        request = MagicMock(data={'username': 'lisi', 'password': 'lisi'},
                            isPermissioned=True)
        middleware_isvalid_method.return_value = False
        response = login.views.Login().post(request)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        # fifth case
        request = MagicMock(data={'username': 'lisi', 'password': 'lisi'},
                            isPermissioned=False)
        middleware_isvalid_method.return_value = False
        response = login.views.Login().post(request)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLogoffView(TestCase):

    def setUp(self):
        self.obj1 = login.views.Logoff()
        self.obj2 = login.views.Logoff()

        self.permission = KSMP_Permission()
        self.zhangsan = self.permission.set_permission('zhangsan')
        self.lisi = self.permission.set_permission('lisi')

    def tearDown(self):
        session.permission.AuthList = {}

    def test_post(self):
        # ksmp_permission_method.return_value = MagicMock(get_permission=lambda auth: auth)
        # first case
        request = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: self.zhangsan})

        response = self.obj1.post(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, 'logout success.')

        # second case
        request = MagicMock(COOKIES={})
        response = self.obj1.post(request)
        self.assertEquals(response.data, 'never login.')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # third case
        request = MagicMock(COOKIES={settings.SESSION_COOKIE_NAME: 'fneiwapure'})
        response = self.obj1.post(request)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, 'logout success.')
