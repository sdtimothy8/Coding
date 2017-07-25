"""
Purpose: Provide public method for ft/log module.
"""
import re
import sys
import os
from ksmp import message
from ksmp import util

__author__ = 'yuxiubj@inspur.com'

reload(sys)
sys.setdefaultencoding("utf-8")

MSG_FILE_TYPE_UNACCEPT = "The upload file type is unacceptable"
MSG_FILE_NAME_INCORRECT = "The upload file name is incorrect"
MSG_FILE_SIZE_OVER = "File size is out of range"
MSG_OK = "OK"
MSG_EXCEPT = "some except happen"
MSG_MAKEPATH_EXIT = "path exit"


class FilePubServ():
    """
    The business class for operating file.
    """

    def __init__(self):
        pass

    @classmethod
    def upload_file(cls, f, fn):
        # upload file
        dest = open(fn, 'w')
        for chunk in f.chunks():
            dest.write(chunk)
        dest.close()
        return message.ADD_SUCCESS

    @classmethod
    def file_name_validity(cls, file_name):
        """
        upload file.
        :param file_name:
        :return:
        """
        rux = u"(^[\w\u4e00-\u9fa5]{1}[^\\\/\&\?\#]+$)"
        pattern = re.compile(rux)
        match_flag = re.match(pattern, file_name.decode("utf-8"))
        if match_flag is None:
            return False, MSG_FILE_NAME_INCORRECT
        return True, MSG_OK

    @classmethod
    def make_path(cls, file_path):
        # make dir
        if file_path is None:
            return False, message.DIR_NOT_EXISTS
        if 0 == os.path.isdir(file_path):
            os.makedirs(file_path)
        return True, MSG_OK

    @classmethod
    def check_filesize(cls, f):
        # check filesize, can't exceed 500M limit
        if f.size > 500000000:
            return False, MSG_FILE_SIZE_OVER
        return True, MSG_OK

    @classmethod
    def rule_filename(cls, file_name):
        if(file_name is None or file_name.strip() == ""):
            return False, MSG_FILE_NAME_INCORRECT
        n_pos = file_name.rfind("\\")
        if(n_pos == -1):
            rule_name = file_name
        else:
            rule_name = file_name[n_pos+1:]
        return True, rule_name
