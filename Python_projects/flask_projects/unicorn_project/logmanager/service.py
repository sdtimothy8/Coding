"""
Purpose: Provide all of the method for ft module.
"""
from ksmp import message
from ksmp import util
from ksmp import settings
from ksmp import logger
import re

__author__ = 'zhangguolei@inspur.com'


class LogDetailBusiness():
    """
    The business class for operating logDetail.
    """

    def __init__(self):
        pass

    @classmethod
    def view_kernellogdetail_get(cls, request):
        """
        Get kernel log detail.
        """
        try:
            offset = int(request.GET['offset'])
            limit = int(request.GET['limit'])
            if request.GET['order'] == 'asc':
                desc = False
            else:
                desc = True
        except Exception:
            offset = 0
            limit = 10
            desc = True

        try:
            search = request.GET['search']
        except Exception:
            search = None
        try:
            # get file detail

            retstr = cls.view_log_detail(limit, offset, desc, search)
            return True, retstr

        except Exception, e:
            logger.error(e)
            return False, util.getResult(message.RESULT_TYPE_ERROR, message.FILE_NOT_EXISTS)

    @classmethod
    def view_unicornlogdetail_get(cls):
        """
        Get unicorn log detail.
        """
        try:
            # get file detail

            retstr = cls.log_unicorn_detail()
            return True, retstr

        except Exception, e:
            logger.error(e)
            return False, util.getResult(message.RESULT_TYPE_ERROR, message.FILE_NOT_EXISTS)

    @classmethod
    def view_log_detail(cls, limit, offset, desc, search):
        """
        get file detail
        :param limit: page size
        :param offset: page start
        :param desc:
        :param search: saerch
        :return: file detail
        """
        logger.debug("init view log detail")
        p = settings.LOG_ROOT_PATH + settings.KERNEL_LOG_NAME
        p = p.encode(settings.DEFAULT_CHARSET)

        f = open(p, 'rb')

        if desc:
            count, page_list = cls.log_kdesc_detail(f, limit, offset, search)
        else:
            count, page_list = cls.log_kdetail(f, limit, offset, search)

        result = {"total": count, "rows": page_list}
        if f:
            f.close()
        return result

    @classmethod
    def log_unicorn_detail(cls):
        """
        get desc detail
        """
        p = settings.LOG_ROOT_PATH + settings.UNICORN_LOG_NAME
        p = p.encode(settings.DEFAULT_CHARSET)

        f = open(p, 'rb')
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
        count = 0
        page_list = []
        for content in f.readlines():
            if (content is None):
                break
            if pattern.match(content):
                lines = content.split(" ", 3)

                page_list.append(dict({"date": lines[0] + " " + lines[1], "level": lines[2][1:-1], "levelnum":
                                 cls.get_level_num(lines[2][1:-1]), "content": lines[3]}))
            else:
                page_list[-1]["content"] = page_list[-1]["content"] + "<br/>" + content

        return page_list

    @classmethod
    def get_level_num(cls, level):
        """
        get level num
        :param level: level
        :return: ERROR:4 ; WARNING:3;INFO:2;DEBUG:1
        """
        if level == 'ERROR':
            return 4
        elif level == "WARNING":
            return 3
        elif level == "INFO":
            return 2
        elif level == "DEBUG":
            return 1
        else:
            return 0

    @classmethod
    def log_kdesc_detail(cls, f, limit, offset, search):
        """
        get desc detail
        :param f: file
        :param limit: page size
        :param offset: page start
        :param search: search
        :return: file detail
        """
        count = 0
        page_list = []
        for line in reversed(f.readlines()):
            if (line is None):
                break
            if search and search not in line:
                    continue
            if count >= offset + limit:
                count += 1
                continue
            if count < offset:
                count += 1
                continue
            page_list.append({"date": line[0:15], "content": line[16:]})
            # print line
            count += 1
        return count, page_list

    @classmethod
    def log_kdetail(cls, f, limit, offset, search):
        """
        get kernel detail
        :param f: file
        :param limit: page size
        :param offset: page start
        :param search: search
        :return: file detail
        """

        count = 0
        page_list = []
        for content in f.readlines():
            if (content is None):
                break
            if search and search not in content:
                    continue
            if count >= offset + limit:
                count += 1
                continue
            if count < offset:
                count += 1
                continue

            page_list.append({"date": content[0:15], "content": content[16:]})
            count += 1
        return count, page_list
