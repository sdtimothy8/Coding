'''
this module is used to provide an storage engine for django session middleware
'''
import time
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings
from session.permission import KSMP_Permission


class SessionStore(SessionBase):
    """
    implement session store.
    """

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        '''
        load all AuthCode from service
        '''
        ksmpcrypt = KSMP_Permission()
        authlist = ksmpcrypt.get_all_auth()
        key = self.session_key
        token = ksmpcrypt.get_permission(key)
        if token in authlist:
            return token
        self.create()
        return {}

    def exists(self, session_key):
        '''
        judge whether a session_key is existed
        :param: session_key is string with hex code
        :return: boolean
        '''
        pms = KSMP_Permission()
        authlist = pms.get_all_auth()
        return pms.get_permission(session_key) in authlist

    def create(self):
        '''
        set object's properties
        '''
        self._session_key = None
        self.modified = True
        self._session_cache = {}
        return

    def save(self, must_create=False):
        '''
        update authcode expire time and save to AuthList
        '''
        current_time = time.time()
        if self.session_key is None:
            return
        permission = KSMP_Permission()
        # AuthList = permission.get_all_auth()
        auth = permission.get_permission(self.session_key)
        permission.save_to_auth(auth, current_time)
        # AuthList[auth] = current_time

    def delete(self, session_key=None):
        '''
        delete session_key form AuthList
        '''
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        permission = KSMP_Permission()
        permission.delete_auth(permission.get_permission(session_key))

    @classmethod
    def clear_expired(cls):
        '''
        delete expired authcode from AuthList
        '''
        EXPIRE_TIME = settings.SESSION_COOKIE_AGE
        ksmpcrypt = KSMP_Permission()
        authlist = ksmpcrypt.get_all_auth()
        items = []
        for item in authlist:
            if (time.time() - authlist[item]) > EXPIRE_TIME:
                items.append(item)
        for item in items:
            try:
                del authlist[item]
            except KeyError:
                pass
