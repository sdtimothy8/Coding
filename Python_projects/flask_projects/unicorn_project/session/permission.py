'''
this module is used for AuthenticateCodes' create, delete, save, encode and decode
'''
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random
import time
from django.conf import settings
from models import Auths


class KSMP_Permission(object):
    '''
    preceeding class for AuthList
    '''
    def __init__(self):
        '''
        initiate object properties
        '''
        self.key = settings.PERMISSION_KEY  # 16 bytes
        self.mode = AES.MODE_ECB
        self.prefix = settings.PERMISSION_PREFIX

    def set_permission(self, text):
        '''
        params: text allways is username 16*n bytes
        return: encoded auth code
        '''
        length = 32
        if len(text) > length:
            return ''
        text = ''.join(random.sample(self.prefix, length - len(text))) + text
        encryptor = AES.new(self.key, self.mode)

        current_time = time.time()

        self.save_to_auth(text, current_time)

        ciphertext = encryptor.encrypt(text)

        return b2a_hex(ciphertext)

    def get_permission(self, encrypt_text):
        '''
        params: encrypt_text string with hex values
        return: drypte text
        '''
        decryptor = AES.new(self.key, self.mode)
        try:
            decrypttext = decryptor.decrypt(a2b_hex(encrypt_text))
        except TypeError:
            return None
        return decrypttext

    def get_all_auth(self):
        '''
        return all content in AuthList
        '''
        AuthList = {}
        proc = Auths.objects.all()
        for i in range(len(proc)):
            auth = proc[i].authcode
            access_time = proc[i].access_time
            AuthList[auth] = float(access_time)
        return AuthList
        # return AuthList

    def save_to_auth(self, auth, current_time=None):
        '''
        if current_time existed save auth into AuthList with time is current time
        other update the auth's time as current_time
        '''
        current_time = current_time if current_time else time.time()
        if (type(auth) is unicode or type(auth) is str)and type(current_time) is float:
            try:
                proc = Auths.objects.get(authcode=auth)
            except Auths.objects.model.DoesNotExist:
                proc = Auths(authcode=auth, access_time=current_time)
                proc.save()
            else:
                proc.access_time = current_time
                proc.save()
            # AuthList[auth] = current_time
        else:
            raise TypeError

    def delete_auth(self, auth):
        '''
        remove an auth from Authlist
        confirm the AuthList not content this auth
        '''
        try:
            proc = Auths.objects.get(authcode=auth)
        except Auths.objects.model.DoesNotExist:
            pass
        else:
            proc.delete()
        return True
