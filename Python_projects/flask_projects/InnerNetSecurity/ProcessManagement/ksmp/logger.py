import logging


__author__ = 'zhangguolei'


def info(message, *args, **kwargs):
    """
    info log
    :param message:
    :param args:
    :param kwargs:
    :return:
    """
    getLogger().info(message, *args, **kwargs)


def debug(message, *args, **kwargs):
    """
    debug log
    :param message:
    :param args:
    :param kwargs:
    :return:
    """
    getLogger().debug(message, *args, **kwargs)


def error(message, *args, **kwargs):
    """
    error log
    :param message:
    :param args:
    :param kwargs:
    :return:
    """
    getLogger().error(message, *args, **kwargs)


def warning(message, *args, **kwargs):
    """
    warning log
    :param message:
    :param args:
    :param kwargs:
    :return:
    """
    getLogger().warning(message, *args, **kwargs)


def getLogger():
    """
    init logger
    :return:
    """
    return logging.getLogger('django')
