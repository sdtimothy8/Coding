"""
Purpose: Provide all of the method for ft module.
"""
from ksmp import message
from ksmp import util
from ksmp import settings
from ft import common
import time
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
__author__ = 'yuxiubj@inspur.com'

LINE_PAGE_NUM = 100


class LogBusiness():
    """
    The business class for operating logList.
    """

    def __init__(self):
        pass

    @classmethod
    def upload_file_post(cls, request):
        """
        upload file.
        :param request:
        :return:
        """
        try:
            if request.GET == 0:
                return False, message.PATH_CONTAIN_ILLEGAL_CHAR

            # don't allow to access parent directory
            p = None
            if request.GET.get('path'):
                p = request.GET['path']
                if p.find('..') >= 0:
                    return False, message.PATH_CONTAIN_ILLEGAL_CHAR

            # check file size,range 0-500MB,file type is text
            retflg, retstr = cls.check_file(request.FILES['file'])
            if not retflg:
                return retflg, retstr

            # delete the file path to get file name
            retflg, retstr = common.FilePubServ.rule_filename(request.data['fileName'])
            if not retflg:
                return retflg, retstr
            file_name = retstr

            # check file name
            retflg, retstr = common.FilePubServ.file_name_validity(file_name)
            if not retflg:
                return retflg, retstr

            # access dir and upload file
            if p:
                fp = settings.LOG_ROOT_PATH + p + '/'
            else:
                fp = settings.LOG_ROOT_PATH
            fn = fp + file_name
            fn = fn.encode(settings.DEFAULT_CHARSET)

            if p is not None and os.path.isdir(fp) == 0:
                return False, message.DIR_NOT_EXISTS

            if fn:
                if os.path.exists(fn):
                    return False, message.FILE_EXISTS
                retstr = common.FilePubServ.upload_file(request.FILES['file'], fn)
                return True, retstr
        except:
            return False, common.MSG_EXCEPT

    @classmethod
    def log_dir_list_get(cls, request):
        """
        get list for dir
        """
        # don't allow to access parent directory
        p = None
        if request.GET.get('path'):
            p = request.GET['path']
            if p.find('..') >= 0:
                return False, message.PATH_CONTAIN_ILLEGAL_CHAR
        try:
            # get list
            result = cls.get_log_list(p)
            return True, result
        except os.error:
            return False, common.MSG_EXCEPT

    @classmethod
    def check_file(cls, f):
        # check file size, can't exceed 500M limit
        if not cls.is_text(f.content_type):
            return False, common.MSG_FILE_TYPE_UNACCEPT
        return common.FilePubServ.check_filesize(f)

    @classmethod
    def is_text(cls, cont_type):
        type_str = cont_type.encode(settings.DEFAULT_CHARSET)
        type_str = type_str.strip().lower()
        if type_str.startswith("text"):
            return True
        return False

    @classmethod
    def get_log_list(cls, p):
        # get list for dir
        if p:
            p = settings.LOG_ROOT_PATH + p + '/'
        else:
            p = settings.LOG_ROOT_PATH
        list_dir = os.listdir(p)
        list_dir.sort(key=lambda a: a.lower())
        list_str = []

        for path in list_dir:
            full_path = p + path
            if os.path.isdir(full_path):
                list_str.append({"name": path, "is_dir": os.path.isdir(full_path)})
            else:
                ok_size = cls.if_size_ok(full_path)
                list_str.append({"name": path, "is_dir": os.path.isdir(full_path), "f_size": ok_size})

        result = {"path": p, "logs": list_str}
        return result

    @classmethod
    def if_size_ok(cls, full_path):
        file_size = os.path.getsize(full_path)
        if file_size > 500000000:
            ok_size = False
        else:
            ok_size = True
        return ok_size


class LogDetailBusiness():
    """
    The business class for operating logDetail.
    """

    def __init__(self):
        pass

    @classmethod
    def view_logdetail_get(cls, request, itemid):
        """
        Get log detail.
        """
        content = None
        path = None

        # deal with input parameters
        try:
            length = int(request.GET['length'])
        except Exception:
            length = 0
        try:
            page = int(request.GET['page'])
        except Exception:
            page = 1

        if page < 1:
            return False, "page num error."

        if request.GET.get('content'):
            content = request.GET['content']

        # don't allow to access parent directory
        if request.GET.get('path'):
            path = request.GET['path']
            if path.find('..') >= 0:
                return False, message.PATH_CONTAIN_ILLEGAL_CHAR
        try:
            # get file detail
            if path:
                    p = settings.LOG_ROOT_PATH + path + '/' + itemid
            else:
                    p = settings.LOG_ROOT_PATH + itemid
            p = p.encode(settings.DEFAULT_CHARSET)

            if os.path.isdir(p) or not os.path.exists(p):
                return False, message.FILE_NOT_EXISTS

            retstr = cls.view_log_detail(p, length, content)
            return True, retstr
        except:
            return False, common.MSG_EXCEPT

    @classmethod
    def delete_log(cls, request, itemid):
        """
        Delete selected log.
        """
        try:
            # don't allow to access parent directory
            path = None
            if request.GET.get('path'):
                path = request.GET['path']
                if path.find('..') >= 0:
                    return False, message.PATH_CONTAIN_ILLEGAL_CHAR

            # delete log file
            if path:
                p = settings.LOG_ROOT_PATH + path + '/' + itemid
            else:
                p = settings.LOG_ROOT_PATH + itemid
            p = p.encode(settings.DEFAULT_CHARSET)

            if os.path.isfile(p):
                os.remove(p)
                return True, message.DELETE_SUCCESS
            else:
                return False, message.FILE_NOT_EXISTS
        except:
            return False, common.MSG_EXCEPT

    @classmethod
    def view_log_detail(cls, p, length, content):
        # get file detail
        list_line = []
        start_time = time.time()
        if length == 0:
            line_num = 1000
        else:
            # when length>0 then tail -n filename |grep content
            line_num = length
        command = "tail -" + str(line_num) + " " + p
        if content:
            command = command + " | grep " + content

        for line in os.popen(command).readlines():
            list_line.append(line)
        end_time = time.time()
        elasped = end_time - start_time
        ret_str = {"length": length, "content": content, "extime": elasped, "logs": list_line}
        return ret_str

    @classmethod
    def get_file_nums(cls, filename):
        command = "wc -l " + filename
        con_list = os.popen(command).readline().strip().split()
        file_length = con_list[0]
        return int(file_length)


def create_temp(fn):
    # create temp file
    if not os.path.exists(fn):
        f = open(fn, 'w')
        f.write("write file!!!")
        f.close()


def delete_file(fn):
    # delete file
    if os.path.exists(fn):
        os.remove(fn)
