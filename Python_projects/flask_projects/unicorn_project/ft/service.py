"""
Purpose: Provide all of the method for ft module.
"""
from django.http import HttpResponse
from ksmp import message
from ksmp import util
from ksmp import settings
import common
import os
import sys
import datetime
from ksmp import logger


__author__ = 'yuxiubj@inspur.com'

reload(sys)
sys.setdefaultencoding("utf-8")


class FileBusiness():
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
            up_path = None

            # only upload to settings.FILETRANS_ROOT_PATH,else return error
            if request.GET.get('path'):
                up_path = request.GET['path']
                if up_path.find('..') >= 0:
                    return False, message.PATH_CONTAIN_ILLEGAL_CHAR

            # check file size,range 0-500MB
            retflg, retstr = common.FilePubServ.check_filesize(request.FILES['file'])
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

            # upload file
            if up_path:
                file_path = settings.FILETRANS_ROOT_PATH + up_path + '/'
            else:
                file_path = settings.FILETRANS_ROOT_PATH

            retflg, retstr = common.FilePubServ.make_path(file_path)
            if not retflg:
                return retflg, retstr

            fn = file_path + file_name
            fn = fn.encode(settings.DEFAULT_CHARSET)

            if fn:
                if os.path.exists(fn):
                    return False, message.FILE_EXISTS
                retstr = common.FilePubServ.upload_file(request.FILES['file'], fn)
                return True, retstr
        except Exception, e:
            logger.error("upload failed! : {}".format(str(e)))
            return False, common.MSG_EXCEPT

    @classmethod
    def ft_dir_list_get(cls, request):
        # only upload to settings.FILETRANS_ROOT_PATH,else return error
        p = None
        if request.GET.get('path'):
            p = request.GET['path']
            if p.find('..') >= 0:
                return False, message.PATH_CONTAIN_ILLEGAL_CHAR
        try:
            result = cls.get_ft_list(p)
            return True, result
        except os.error:
            return False, common.MSG_EXCEPT

    @classmethod
    def get_ft_list(cls, p):
        # get list for dir
        if p:
            p = settings.FILETRANS_ROOT_PATH + p
        else:
            p = settings.FILETRANS_ROOT_PATH

        list_dir = os.listdir(p)
        list_dir.sort(key=lambda a: a.lower())
        list_str = []

        for path in list_dir:
            full_path = p + path
            if os.path.isdir(full_path):
                list_str.append({"name": path, "is_dir": os.path.isdir(full_path)})
            else:
                file_size = cls.get_filesize(os.path.getsize(full_path))
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
                list_str.append({"name": path, "is_dir": os.path.isdir(full_path), "f_size": file_size, "f_time": file_time})
        result = {"path": p, "fts": list_str}
        return result

    @classmethod
    def get_filesize(cls, size):
        # get file size
        if size >= 1000000:
            return "%.1f MB" % (size / 1000000.0)
        elif 1000 <= size < 1000000:
            return "%.1f KB" % (size / 1000.0)
        else:
            return "%d bytes" % size


class FileDetailBusiness():
    """
    The business class for operating logDetail.
    """

    def __init__(self):
        pass

    @classmethod
    def download_file_get(cls, request, itemid):
        """
        download file
        """
        if request.GET == 0:
            return False, message.PATH_CONTAIN_ILLEGAL_CHAR
        up_path = None

        # only upload to settings.FILETRANS_ROOT_PATH,else return error
        if request.GET.get('path'):
            up_path = request.GET['path']
            if up_path.find('..') >= 0:
                return False, message.PATH_CONTAIN_ILLEGAL_CHAR

        # download file
        try:
            if up_path:
                file_path = settings.FILETRANS_ROOT_PATH + up_path + '/'
            else:
                file_path = settings.FILETRANS_ROOT_PATH

            # if dir not exist,make file path
            retflg, retstr = common.FilePubServ.make_path(file_path)
            if not retflg:
                return retflg, retstr
            filename = itemid.encode(settings.DEFAULT_CHARSET)
            fn = file_path + filename

            if fn:
                if not os.path.exists(fn):
                    return False, message.FILE_NOT_EXISTS
                resp = HttpResponse(cls.download_file(fn), content_type='application/octet-stream')
                resp['Content-Disposition'] = "attachment; filename=%s" % filename
                return True, resp
        except os.error:
            return False, common.MSG_EXCEPT

    @classmethod
    def download_file(cls, fn, chunk_size=1024):
        # download file
        f = open(fn, 'r')
        while True:
            dest = f.read(chunk_size)
            if dest:
                yield dest
            else:
                break


def creat_file(fn):
    # create temp file
    if not os.path.exists(fn):
        f = open(fn, 'w')
        f.write("write file!!!")
        f.close()


def delete_file(fn):
    # delete file
    if os.path.exists(fn):
        os.remove(fn)
