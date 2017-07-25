# coding=utf-8
import os
import fcntl
import uuid

__author__ = 'liushaolin@inspur.com'


class VNCToken(object):
    """
    VNCToken class is used to manage vnc token.
    Class method 'save_token' is used to save a unique token string for a virtual machine when it's created.
    Class method 'get_now_port' is used to get the latest port from vnc token configure file
    Class method 'get_port_by_token' is used to get the port of a virtual machine from vnc token configure file
    by its token string.
    """
    TOKEN_PATH = os.path.join(os.path.dirname(__file__), './vnc_tokens/vnc-1.ini')
    LOCAL_HOST = ' 127.0.0.1'    # Pay attention to the blank space

    @classmethod
    def init_token(cls):
        if not os.path.exists(VNCToken.TOKEN_PATH):
            try:
                with open(VNCToken.TOKEN_PATH, "w+") as f:
                    vnc_line = ':'.join([str(uuid.uuid4()), VNCToken.LOCAL_HOST, '15899'])
                    f.write(vnc_line + '\n')
            except Exception, e:
                print ("init virtual machine token failed: {0}".format(e))
        else:
            pass

    @classmethod
    def save_token(cls, token, port):
        cls.init_token()
        try:
            with open(VNCToken.TOKEN_PATH, "a+") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                # now_port = int(f.readlines()[-1].split(':')[-1])
                # new_port = now_port + 1
                vnc_line = ':'.join([token, VNCToken.LOCAL_HOST, str(port)])
                f.write(vnc_line + '\n')
        except Exception, e:
            print ("save virtual machine token failed: {0}".format(e.message))

    @classmethod
    def get_now_port(cls):
        """
        Get the latest port in vnc token configure file in the last line.
        :return:
        """
        cls.init_token()
        try:
            with open(VNCToken.TOKEN_PATH, "a+") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                now_port = int(f.readlines()[-1].split(':')[-1])
                return now_port + 1
        except Exception, e:
            print ("get virtual machine port failed: {0}".format(e.message))
            return None

    @classmethod
    def get_port_by_token(cls, token):
        """
        Get port with token.
        :param token:
        :return:
        """
        cls.init_token()
        try:
            with open(VNCToken.TOKEN_PATH, "a+") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                for line in f:
                    vnc_list = line.split(':')
                    if vnc_list[0] == token:
                        return vnc_list[-1]
                return None
        except Exception, e:
            print ("save virtual machine token failed: {0}".format(e.message))
            return None
