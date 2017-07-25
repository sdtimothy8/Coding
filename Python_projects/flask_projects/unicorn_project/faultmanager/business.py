# coding:utf-8
import datetime
import os
from itertools import chain
from operator import itemgetter
from string import strip
import commands
from faultmanager.models import CpuEvents, MemEvents, DiskEvents, RepEvents, PcieEvents, NetEvents, XfsEvents, MdEvents
from faultmanager.models import BmcEvents, LockEvents, KdumpEvents, DevScore, DevStatus, Email
from faultmanager import constr
from ksmp import logger
from public import functions
from ft.common import FilePubServ
from ksmp import settings
import time


__author__ = 'zhuysh@inspur.com'


class CountBusiness():

    @classmethod
    def evt_count(cls, qtype=constr.QUERY_EVT, **kwargs):

        starttime = datetime.datetime.strptime(kwargs[constr.START_TIME], '%Y-%m-%d').date()
        endtime = datetime.datetime.strptime(kwargs[constr.END_TIME], '%Y-%m-%d').date() + datetime.timedelta(days=1)

        if constr.QUERY_EVT == qtype:
            evts_count = {}
            try:
                # # cpu evt level count
                # cpu_critical = CpuEvents.objects.filter(evt_level='Critical').count()
                # cpu_major = CpuEvents.objects.filter(evt_level='Major').count()
                # cpu_minor = CpuEvents.objects.filter(evt_level='Minor').count()
                # cpu_trivial = CpuEvents.objects.filter(evt_level='Trivial').count()
                #
                # # mem evt level count
                # mem_critical = MemEvents.objects.filter(evt_level='Critical').count()
                # mem_major = MemEvents.objects.filter(evt_level='Major').count()
                # mem_minor = MemEvents.objects.filter(evt_level='Minor').count()
                # mem_trivial = MemEvents.objects.filter(evt_level='Trivial').count()
                #
                # # disk evt level count
                # disk_critical = DiskEvents.objects.filter(evt_level='Critical').count()
                # disk_major = DiskEvents.objects.filter(evt_level='Major').count()
                # disk_minor = DiskEvents.objects.filter(evt_level='Minor').count()
                # disk_trivial = DiskEvents.objects.filter(evt_level='Trivial').count()
                #
                # evts_count = {
                #     'Critical': int(cpu_critical) + int(mem_critical) + int(disk_critical),
                #     'Major': int(cpu_major) + int(mem_major) + int(disk_major),
                #     'Minor': int(cpu_minor) + int(mem_minor) + int(disk_minor),
                #     'Trivial': int(cpu_trivial) + int(mem_trivial) + int(disk_trivial)
                # }

                for dev in constr.MONITOR_DEV:
                    flag, evts_count[dev] = cls.time_count(dev, **kwargs)
                    if not flag:
                        return False, constr.FAULT_FAIL

            except Exception, e:
                logger.error("CountBusiness(ALL) ERROR : " + str(e.message))
                return False, None

            return True, sorted(cls.__format_evt_counts(starttime, endtime, evts_count).iteritems(), key=lambda d: d[0])

        elif constr.QUERY_DEV == qtype:

            try:
                # cpu evt count
                cpu_count = CpuEvents.objects.filter(timestamp__range=(starttime, endtime)).count()
                # mem evt count
                mem_count = MemEvents.objects.filter(timestamp__range=(starttime, endtime)).count()
                # disk evt count
                disk_count = DiskEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                pcie_count = PcieEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                net_count = NetEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                xfs_count = XfsEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                bmc_count = BmcEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                # mpio_count = MpioEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                # apei_count = ApeiEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                lock_count = LockEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                # memt_count = MemtEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                # loga_count = LogaEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                kdump_count = KdumpEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                md_count = MdEvents.objects.filter(timestamp__range=(starttime, endtime)).count()

                evts_count = {
                    'cpu': cpu_count,
                    'mem': mem_count,
                    'disk': disk_count,
                    'pcie': pcie_count,
                    'net': net_count,
                    'xfs': xfs_count,
                    'bmc': bmc_count,
                    # 'mpio': mpio_count,
                    # 'apei': apei_count,
                    'lock': lock_count,
                    # 'memt': memt_count,
                    # 'loga': loga_count,
                    'kernel': kdump_count,
                    'md': md_count
                }

            except Exception, e:
                logger.error("CountBusiness(" + str(qtype) + ") ERROR : " + str(e.message))
                return False, None

            return True, evts_count

        else:

            try:
                # # args init
                # starttime = datetime.datetime.strptime(kwargs[constr.START_TIME], '%Y-%m-%d').date()
                # endtime = datetime.datetime.strptime(kwargs[constr.END_TIME], '%Y-%m-%d').date() + datetime.timedelta(days=1)
                #
                # # CPU evt count
                # if constr.QUERY_CPU == qtype:
                #     data = CpuEvents.objects.filter(time__range=(starttime, endtime))
                # elif constr.QUERY_MEM == qtype:
                #     data = MemEvents.objects.filter(time__range=(starttime, endtime))
                # else:
                #     data = DiskEvents.objects.filter(time__range=(starttime, endtime))
                #
                # critical = data.filter(evt_level='Critical').count()
                # major = data.filter(evt_level='Major').count()
                # minor = data.filter(evt_level='Minor').count()
                # trivial = data.filter(evt_level='Trivial').count()
                #
                # evts_count = {
                #     'Critical': int(critical),
                #     'Major': int(major),
                #     'Minor': int(minor),
                #     'Trivial': int(trivial)
                # }
                flag, evts_count = cls.time_count(qtype, **kwargs)
                if not flag:
                    return False, constr.FAULT_FAIL

            except Exception, e:
                logger.error("CountBusiness(" + str(qtype) + ") ERROR : " + str(e.message))
                return False, None

            return True, sorted(evts_count.iteritems(), key=lambda d: d[0])

    @classmethod
    def dev_count(cls, dev, **kwargs):
        """
        query dev faults info
        :param dev: cpu mem disk and so on
        :param kwargs: start_time end_time
        :return: faults count
        """

        rtn_info = {}

        starttime = datetime.datetime.strptime(kwargs[constr.START_TIME], '%Y-%m-%d').date()
        endtime = datetime.datetime.strptime(kwargs[constr.END_TIME], '%Y-%m-%d').date() + datetime.timedelta(days=1)

        try:

            if dev == constr.QUERY_CPU:
                data = CpuEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif dev == constr.QUERY_MEM:
                data = MemEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif dev == constr.QUERY_DISK:
                data = DiskEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_PCIE == dev:
                data = PcieEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_NET == dev:
                data = NetEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_XFS == dev:
                data = XfsEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_BMC == dev:
                data = BmcEvents.objects.filter(timestamp__range=(starttime, endtime))
            # elif constr.QUERY_MPIO == dev:
            #     data = MpioEvents.objects.filter(timestamp__range=(starttime, endtime))
            # elif constr.QUERY_APEI == dev:
            #     data = ApeiEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_LOCK == dev:
                data = LockEvents.objects.filter(timestamp__range=(starttime, endtime))
            # elif constr.QUERY_MEMT == dev:
            #     data = MemtEvents.objects.filter(timestamp__range=(starttime, endtime))
            # elif constr.QUERY_LOGA == dev:
            #     data = LogaEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_KERNEL == dev:
                data = KdumpEvents.objects.filter(timestamp__range=(starttime, endtime))
            elif constr.QUERY_MD == dev:
                data = MdEvents.objects.filter(timestamp__range=(starttime, endtime))
            else:
                pass
                return False, constr.FAULT_ARGS_ERROR

            critical = data.filter(evt_level='Critical').count()
            major = data.filter(evt_level='Major').count()
            minor = data.filter(evt_level='Minor').count()
            trivial = data.filter(evt_level='Trivial').count()

            rtn_info = {
                'Critical': int(critical),
                'Major': int(major),
                'Minor': int(minor),
                'Trivial': int(trivial)
            }

        except Exception, e:
            logger.error("__dev_count {} count error : ".format(dev, str(e.message)))
            return False, constr.FAULT_FAIL

        return True, rtn_info

    @classmethod
    def time_count(cls, dev, **kwargs):
        """
        count dev fault for period of time
        :param dev:
        :param kwargs:
        :return:
        """

        starttime = datetime.datetime.strptime(kwargs[constr.START_TIME], '%Y-%m-%d').date()
        endtime = datetime.datetime.strptime(kwargs[constr.END_TIME], '%Y-%m-%d').date() + datetime.timedelta(days=1)

        try:
            if constr.QUERY_CPU == dev:
                data = CpuEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                             "COUNT (*) as count "
                                             "FROM cpu_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                             "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                             "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                             [starttime, endtime])
            elif constr.QUERY_MEM == dev:
                data = MemEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                             "COUNT (*) as count "
                                             "FROM mem_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                             "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                             "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                             [starttime, endtime])
            elif constr.QUERY_DISK == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM disk_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            elif constr.QUERY_PCIE == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM pcie_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            elif constr.QUERY_NET == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM net_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            elif constr.QUERY_XFS == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM xfs_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            elif constr.QUERY_BMC == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM bmc_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            # elif constr.QUERY_MPIO == dev:
            #     data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
            #                                   "COUNT (*) as count "
            #                                   "FROM mpio_event WHERE TIMESTAMP BETWEEN %s AND %s "
            #                                   "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
            #                                   "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
            #                                   [starttime, endtime])
            # elif constr.QUERY_APEI == dev:
            #     data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
            #                                   "COUNT (*) as count "
            #                                   "FROM apei_event WHERE TIMESTAMP BETWEEN %s AND %s "
            #                                   "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
            #                                   "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
            #                                   [starttime, endtime])
            elif constr.QUERY_LOCK == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM lock_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            # elif constr.QUERY_MEMT == dev:
            #     data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
            #                                   "COUNT (*) as count "
            #                                   "FROM memt_event WHERE TIMESTAMP BETWEEN %s AND %s "
            #                                   "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
            #                                   "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
            #                                   [starttime, endtime])
            # elif constr.QUERY_LOGA == dev:
            #     data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
            #                                   "COUNT (*) as count "
            #                                   "FROM loga_event WHERE TIMESTAMP BETWEEN %s AND %s "
            #                                   "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
            #                                   "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
            #                                   [starttime, endtime])
            elif constr.QUERY_KERNEL == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM kernel_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            elif constr.QUERY_MD == dev:
                data = DiskEvents.objects.raw("SELECT ID, YEAR || '-' || MONTH || '-' || DAY AS datainfo, EVT_LEVEL, "
                                              "COUNT (*) as count "
                                              "FROM md_event WHERE TIMESTAMP BETWEEN %s AND %s "
                                              "GROUP BY (YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL ORDER BY "
                                              "(YEAR || '-' || MONTH || '-' || DAY), EVT_LEVEL",
                                              [starttime, endtime])
            else:
                pass

            rtn_data = {}
            for evt in data:
                key_data = datetime.datetime.strftime(datetime.datetime.strptime(str(evt.datainfo), '%Y-%m-%d').date(),
                                                      '%Y-%m-%d')
                key_level = str(evt.evt_level)
                if key_data in rtn_data:
                    temp = rtn_data[key_data]
                    temp[key_level] = evt.count
                else:
                    rtn_data[key_data] = {key_level: evt.count}

        except Exception, e:
            logger.error("time_count error : {}".format(str(e.message)))
            return False, constr.FAULT_FAIL
        return True, cls.__format_dev_counts(starttime, endtime, rtn_data)

    @staticmethod
    def __format_dev_counts(starttime, endtime, datainfo):
        # days = lambda d: datetime.timedelta(days=d)
        # delta = str(endtime - starttime).split()[0]
        # date_temp = [datetime.datetime.strftime(starttime + days(x), '%Y-%m-%d') for x in range(0, int(delta))]
        date_list = dict.fromkeys(CountBusiness.__format_time_list(starttime, endtime))
        for date in date_list:
            date_list[date] = {constr.CRITICAL: 0, constr.MAJOR: 0, constr.MINOR: 0, constr.TRIVIAL: 0}
            if date in datainfo:
                for level in constr.LEVEL_LIST:
                    if level in datainfo[date]:
                        date_list[date][level] += int(datainfo[date][level])

        return date_list

    @staticmethod
    def __format_evt_counts(starttime, endtime, datainfo):
        date_list = dict.fromkeys(CountBusiness.__format_time_list(starttime, endtime))
        for x in date_list:
            date_list[x] = {constr.CRITICAL: 0, constr.MAJOR: 0, constr.MINOR: 0, constr.TRIVIAL: 0}
        for dev in constr.MONITOR_DEV:
            dev_date = datainfo[dev]
            for date in date_list:
                # date_list[date] = {constr.CRITICAL: 0, constr.MAJOR: 0, constr.MINOR: 0, constr.TRIVIAL: 0}
                for level in constr.LEVEL_LIST:
                    date_list[date][level] += int(dev_date[date][level])

        return date_list

    @staticmethod
    def __format_time_list(starttime, endtime):
        days = lambda d: datetime.timedelta(days=d)
        delta = str(endtime - starttime).split()[0]
        date_temp = [datetime.datetime.strftime(starttime + days(x), '%Y-%m-%d') for x in range(0, int(delta))]
        return date_temp


class EventsDetailBusiness():

    @classmethod
    def evt_detail(cls, qtype=constr.QUERY_RECENT, **kwargs):

        evt_detail = []

        starttime = datetime.datetime.strptime(kwargs[constr.START_TIME], '%Y-%m-%d').date()
        endtime = datetime.datetime.strptime(kwargs[constr.END_TIME], '%Y-%m-%d').date() + datetime.timedelta(days=1)

        try:
            if constr.QUERY_RECENT == qtype:
                # cpu mem disk recent events
                cpu_data = CpuEvents.objects.all().order_by("-timestamp")[:10]
                mem_data = MemEvents.objects.all().order_by("-timestamp")[:10]
                disk_data = DiskEvents.objects.all().order_by("-timestamp")[:10]
                pcied = PcieEvents.objects.all().order_by("-timestamp")[:10]
                netd = NetEvents.objects.all().order_by("-timestamp")[:10]
                xfsd = XfsEvents.objects.all().order_by("-timestamp")[:10]
                bmcd = BmcEvents.objects.all().order_by("-timestamp")[:10]
                # mpiod = MpioEvents.objects.all().order_by("-timestamp")[:10]
                # apeid = ApeiEvents.objects.all().order_by("-timestamp")[:10]
                lockd = LockEvents.objects.all().order_by("-timestamp")[:10]
                # memtd = MemtEvents.objects.all().order_by("-timestamp")[:10]
                # logad = LogaEvents.objects.all().order_by("-timestamp")[:10]
                kdumpd = KdumpEvents.objects.all().order_by("-timestamp")[:10]
                mdd = MdEvents.objects.all().order_by("-timestamp")[:10]
                data = chain(cpu_data, mem_data, disk_data, pcied, netd, xfsd, bmcd, lockd, kdumpd, mdd)

                evt_detail = sorted([(item.time, item.err_msg) for item in data], key=itemgetter(0), reverse=True)[:10]
            elif constr.QUERY_REPAIR == qtype:
                rep_data = RepEvents.objects.all().order_by("-timestamp_rep")[:10]

                evt_detail = [(item.time, item.err_msg) for item in rep_data]

            elif constr.QUERY_LIST == qtype:
                dev = kwargs[constr.QUERY_DEV]
                if constr.QUERY_CPU == dev:
                    data = CpuEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_MEM == dev:
                    data = MemEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_DISK == dev:
                    data = DiskEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_PCIE == dev:
                    data = PcieEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_NET == dev:
                    data = NetEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_XFS == dev:
                    data = XfsEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_BMC == dev:
                    data = BmcEvents.objects.filter(timestamp__range=(starttime, endtime))
                # elif constr.QUERY_MPIO == dev:
                #     data = MpioEvents.objects.filter(timestamp__range=(starttime, endtime))
                # elif constr.QUERY_APEI == dev:
                #     data = ApeiEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_LOCK == dev:
                    data = LockEvents.objects.filter(timestamp__range=(starttime, endtime))
                # elif constr.QUERY_MEMT == dev:
                #     data = MemtEvents.objects.filter(timestamp__range=(starttime, endtime))
                # elif constr.QUERY_LOGA == dev:
                #     data = LogaEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_KERNEL == dev:
                    data = KdumpEvents.objects.filter(timestamp__range=(starttime, endtime))
                elif constr.QUERY_MD == dev:
                    data = MdEvents.objects.filter(timestamp__range=(starttime, endtime))
                else:
                    pass
                    return False, constr.FAULT_ARGS_ERROR
                evt_detail = cls.__evt_format(data, dev=dev)
            elif constr.QUERY_DEV_RECENT == qtype:
                dev = kwargs[constr.QUERY_DEV]
                if constr.QUERY_CPU == dev:
                    data = CpuEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_MEM == dev:
                    data = MemEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_DISK == dev:
                    data = DiskEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_PCIE == dev:
                    data = PcieEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_NET == dev:
                    data = NetEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_XFS == dev:
                    data = XfsEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_BMC == dev:
                    data = BmcEvents.objects.all().order_by("-timestamp")[:10]
                # elif constr.QUERY_MPIO == dev:
                #     data = MpioEvents.objects.all().order_by("-timestamp")[:10]
                # elif constr.QUERY_APEI == dev:
                #     data = ApeiEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_LOCK == dev:
                    data = LockEvents.objects.all().order_by("-timestamp")[:10]
                # elif constr.QUERY_MEMT == dev:
                #     data = MemtEvents.objects.all().order_by("-timestamp")[:10]
                # elif constr.QUERY_LOGA == dev:
                #     data = LogaEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_KERNEL == dev:
                    data = KdumpEvents.objects.all().order_by("-timestamp")[:10]
                elif constr.QUERY_MD == dev:
                    data = MdEvents.objects.all().order_by("-timestamp")[:10]
                else:
                    pass
                    return False, constr.FAULT_ARGS_ERROR
                evt_detail = cls.__evt_format(data, dev=dev)
            elif constr.QUERY_DEV_REPAIR == qtype:
                dev = constr.DEV_NAME.get(kwargs[constr.QUERY_DEV])
                rep_data = RepEvents.objects.all().filter(device_name=dev).order_by("-timestamp_rep")[:10]
                evt_detail = cls.__evt_repair_format(rep_data)
            elif constr.QUERY_DEV_REPAIRLIST == qtype:
                dev = constr.DEV_NAME.get(kwargs[constr.QUERY_DEV])
                rep_data = RepEvents.objects.all().filter(timestamp_rep__range=(starttime, endtime)).filter(device_name=dev)
                evt_detail = cls.__evt_repair_format(rep_data)

        except Exception, e:
            logger.error("CountBusiness(" + str(qtype) + ") ERROR : " + str(e.message))
            return False, str(e.message)

        return True, evt_detail

    @classmethod
    def fualt_detail(cls, faultid):
        return cls.__evt_detail_info(faultid)

    @staticmethod
    def __evt_format(datas, dev=''):
        rtlist = []
        for data in datas:
            evtdict = {
                'time': data.timestamp,
                'errmsg': data.err_msg,
                'errtype': data.err_type,
                'devid': data.dev_id,
                'evtid': data.evt_id,
                'detail': data.detail,
                'evtlevel': data.evt_level,
                'dev': dev
            }
            rtlist.append(evtdict)
        return rtlist

    @staticmethod
    def __evt_repair_format(datas):
        rtlist = []
        for data in datas:
            evtdict = {
                'time': data.timestamp_rep,
                'errmsg': data.err_msg,
                'errtype': data.err_type,
                'devid': data.dev_id,
                'evtid': data.evt_id,
                'dev': data.device_name,
                'action': data.action,
                'errcount': data.err_count
            }
            rtlist.append(evtdict)
        return rtlist

    @staticmethod
    def __evt_detail_info(clsinfo):
        if clsinfo:
            datas = functions.launchcmd('{} {}'.format(constr.FMS_ERR_DETAIL, clsinfo.replace('list', 'ereport'))).readlines()
            evt_detailinfo = {}
            for line in datas:
                info = line.split(':', 1)
                evt_detailinfo[info[0]] = info[1]
            return True, evt_detailinfo
        else:
            return False, constr.FAULT_ARGS_ERROR


class FaultsBusiness():

    @classmethod
    def read_esc(cls, filename="cpu"):

        # esc_file, agent_file = (constr.FAULT_CPUMEM_ESC, constr.FAULT_CPUMEM_AGENT) \
        #     if filename == 'cpumem' else (constr.FAULT_DISK_ESC, constr.FAULT_DISK_AGENT)
        esc_file, agent_file = "{}{}".format(constr.DEV_SO.get(filename), constr.ESC_FILE),\
                               "{}{}".format(constr.DEV_SO.get(filename), constr.AGENT_FILE)

        try:
            esc_data = []
            agent_data = []
            if filename == "mem" and not os.path.exists(constr.FAULT_ESC_PATH + esc_file):
                esc_file = "memory.esc"
            if os.path.exists(constr.FAULT_ESC_PATH + esc_file):
                with open(constr.FAULT_ESC_PATH + esc_file) as esc:
                    esc_data = format_file(esc.readlines())
            if os.path.exists(constr.FAULT_PLUGINS_PATH + agent_file):
                with open(constr.FAULT_PLUGINS_PATH + agent_file) as agent:
                    agent_data = cls.__format_agentfile(agent.readlines())
        except Exception, e:
            logger.error("read_esc error : " + str(e.message))
            return False

        return format_faultlist(esc_data, agent_data)

    @classmethod
    def modify_agent(cls, filename='cpumem', data=[]):

        # agent_file = constr.FAULT_CPUMEM_AGENT if filename == 'cpumem' else constr.FAULT_DISK_AGENT
        agent_file = "{}{}".format(constr.DEV_SO.get(filename), constr.AGENT_FILE)

        try:
            if data and (data[1] or "true" == data[1] or "True" == data[1]):
                with open(constr.FAULT_PLUGINS_PATH + agent_file, 'a') as agent:
                    agent.write("{} {}\n".format(constr.AGENT_KEYWD, data[0]))
            elif data and (not data[1] or "false" == data[1] or "False" == data[1]):
                filterfile = functions.launchcmd("cat " + constr.FAULT_PLUGINS_PATH + agent_file).readlines()
                new_file = []
                for line in filterfile:
                    need_write = True
                    # find the lines that need write to the file
                    # if strip(line).startswith("#"):
                    if not strip(line).startswith("subscribe"):
                        need_write = True
                    elif data[0] in line:
                        need_write = False

                    if need_write:
                        new_file.append(line)

                with open(constr.FAULT_PLUGINS_PATH + agent_file, 'w+') as wfile:
                    wfile.writelines(new_file)

        except Exception, e:
            logger.error("modify_agent error : " + str(e.message))
            return False

        return True

    @classmethod
    def operate_src(cls, filename='srccpu', otype='read', sdata=1):

        # src_file = constr.FAULT_CPUMEM_SRC if filename == 'srccpumem' else constr.FAULT_DISK_SRC
        src_file = "{}{}".format(constr.DEV_SRC_DICT.get(filename), constr.SRC_FILE)
        rtvale = {}
        try:
            if "read" == otype:
                with open(constr.FAULT_PLUGINS_PATH + src_file) as srcfile:
                    src_data = srcfile.readlines()

                    for line in src_data:
                        if strip(line) and not strip(line).startswith("#"):
                            split_data = line.split()
                            if split_data[0] == constr.SRC_KEYWD:
                                rtvale[constr.SRC_KEYWD] = split_data[1]
                                break
            else:
                filterfile = functions.launchcmd("cat " + constr.FAULT_PLUGINS_PATH + src_file).readlines()
                new_file = []
                for line in filterfile:
                    need_write = True
                    # find the lines that need write to the file
                    if strip(line).startswith("#"):
                        need_write = True
                    elif constr.SRC_KEYWD in line:
                        need_write = False

                    if need_write:
                        new_file.append(line)
                    else:
                        new_file.append("{} {}\n".format(constr.SRC_KEYWD, sdata))

                with open(constr.FAULT_PLUGINS_PATH + src_file, 'w+') as srcfile:
                    srcfile.writelines(new_file)
                    return True

        except Exception, e:
            logger.error("operate_src otype={} error : {}".format(otype, str(e.message)))
            return False

        return rtvale

    @classmethod
    def fmtype_query(cls, itemid='cpu'):
        # src_file = constr.FAULT_CPUMEM_MOD if itemid == 'cpumem' else constr.FAULT_DISK_MOD
        src_file = "{}{}".format(constr.DEV_SO.get(itemid), constr.MOD_FILE)
        rtvale = {}
        try:
            if not os.path.exists(constr.FAULT_PLUGINS_PATH + src_file):
                return False
            with open(constr.FAULT_PLUGINS_PATH + src_file) as srcfile:
                src_data = srcfile.readlines()

                for line in src_data:
                    if strip(line) and strip(line).startswith(constr.MOD_KEYWD):
                        split_data = line.split()
                        rtvale['type'] = split_data[1]
                        break

        except Exception, e:
            logger.error("fmtype_query error : {}".format(str(e.message)))
            return False

        return rtvale

    @classmethod
    def fmtype_manager(cls, itemid='cpu', otype='auto', **kwargs):

        # file_name = constr.FAULT_CPUMEM_MOD if itemid == 'cpumem' else constr.FAULT_DISK_MOD
        file_name = "{}{}".format(constr.DEV_SO.get(itemid), constr.MOD_FILE)

        if otype == constr.FAULT_AUTO:
            return cls.__modify_mod(constr.FAULT_PLUGINS_PATH + file_name)
        else:
            if kwargs['fname'] and kwargs['fdata']:
                fname, fdata = kwargs['fname'], kwargs['fdata']
                try:
                    retflg, retstr = FilePubServ.file_name_validity(fname)
                    if not retflg:
                        return retflg, retstr
                    flag, msg = FilePubServ.make_path(constr.FAULT_UPLOAD_PATH)
                    if not flag:
                        return False, msg
                    fn = constr.FAULT_UPLOAD_PATH + fname
                    fn = fn.encode(settings.DEFAULT_CHARSET)

                    if fn:
                        if os.path.exists(fn):
                            return False, constr.FAULT_FILE_EXISTS
                        FilePubServ.upload_file(fdata, fn)
                        return cls.__modify_mod(constr.FAULT_PLUGINS_PATH + file_name, kvalue=constr.FAULT_MANUAL)

                except Exception, e:
                    logger.error("fmtype_manager upload file failed : {}".format(str(e.message)))
                    return False, constr.FAULT_FILE_UPLOAD_FAIL
            else:
                return False, constr.FAULT_FILE_FAIL

        return True, constr.FAULT_SUCESS

    @classmethod
    def monitor_status(cls, **kwargs):
        """
        query monitor status
        :param kwargs: start_time, end_time
        :return: running,serious.slight
        """

        monitor_status_info = cls.__running_check()

        try:

            for dev in constr.MONITOR_DEV:
                if monitor_status_info[dev] == constr.FMS_RUNNING:
                    flag, rtninfo = CountBusiness.dev_count(dev, **kwargs)
                    if flag and rtninfo:
                        monitor_status_info[dev] = cls.__fault_level(rtninfo)

        except Exception, e:
            logger.error("monitor_status failed : {}".format(str(e.message)))
            return False, constr.FAULT_FAIL

        return True, monitor_status_info

    @classmethod
    def fmd_status(cls):
        try:
            statusinfo = functions.launchcmd(constr.FMS_STATUS).readlines()
            if statusinfo:
                for status in statusinfo:
                    if constr.FMS_ACTIVE == strip(status):
                        return True, {"status": constr.FMS_ACTIVE}
                    else:
                        return True, {"status": constr.FMS_INACTIVE}
        except Exception, e:
            logger.error("fmd_status failed! error : {}".format(str(e.message)))
            return False, constr.FAULT_FAIL
        return False

    @staticmethod
    def __fault_level(faultsInfo):

        if int(faultsInfo[constr.CRITICAL]) > 0:
            return constr.FMS_SERIOUS
        elif int(faultsInfo[constr.MAJOR]) + int(faultsInfo[constr.MINOR]) > 0:
            return constr.FMS_SLIGHT
        else:
            return constr.FMS_RUNNING

    @staticmethod
    def __running_check():
        modinfo = functions.launchcmd(constr.FMS_MODINFO).readlines()
        checkinfo = [x.replace("\n", "") for x in modinfo]
        rtn_status = {}
        for dev in constr.MONITOR_DEV:
            # devkey = "cpumem" if dev == constr.QUERY_CPU or dev == constr.QUERY_MEM else dev
            devkey = constr.DEV_SO.get(dev)
            if "{}{}_{}.so".format(constr.FAULT_PLUGINS_PATH, devkey, constr.CONSTR_AGENT) in checkinfo \
                    and "{}{}_{}.so".format(constr.FAULT_PLUGINS_PATH, devkey, constr.CONSTR_SRC) in checkinfo:
                rtn_status[dev] = constr.FMS_RUNNING
            else:
                rtn_status[dev] = constr.FMS_DEAD
        return rtn_status

    @staticmethod
    def __modify_mod(filen, keywd=constr.MOD_KEYWD, kvalue=constr.FAULT_AUTO):

        try:
            if not os.path.exists(filen):
                with open(filen, 'w') as w_mod_file:
                    w_mod_file.writelines("{} {}\n".format(keywd, kvalue))
                    return True, constr.FAULT_SUCESS
            filterfile = functions.launchcmd("cat " + filen).readlines()
            new_file = []
            for line in filterfile:
                need_write = True
                # find the lines that need write to the file
                if strip(line).startswith("#"):
                    need_write = True
                elif keywd in line:
                    need_write = False

                if need_write:
                    new_file.append(line)
                else:
                    new_file.append("{} {}\n".format(keywd, kvalue))

            with open(filen, 'w+') as srcfile:
                srcfile.writelines(new_file)
        except Exception, e:
            logger.error("__modify_mod kvalue {} error : {}".format(kvalue, str(e.message)))
            return False, str(e.message)
        return True, constr.FAULT_SUCESS

    @staticmethod
    def __format_agentfile(file_data):
        rt_data = []

        if file_data:
            for line in file_data:
                if strip(line) and strip(line).startswith("subscribe"):
                    # rt_data.append("event.{}".format(line.split('event.')[1]) if line.split('event.')[1] else "")
                    rt_data.append(line.split()[1] if line.split()[1] else "")

        return rt_data


def format_faultlist(esc_data, agent_data):

    flag = lambda x: x in agent_data

    if esc_data:
        return [[data, flag(data)] for data in esc_data]

    return []


def format_file(file_data):

    rt_data = []

    if file_data:
        for line in file_data:
            if strip(line) and not strip(line).startswith("#") and not strip(line).startswith("*") and not strip(line).startswith("/*")\
                    and (strip(line).startswith("event") or strip(line).startswith("fault") or strip(line).startswith("engine")):
                # rt_data.append("event.{}".format(line.split('ereport.')[1]) if line.split('ereport.')[1] else "")
                rt_data.append("event.{}".format(line.split()[1].replace('ereport.', '')) if line.split()[1] else "")

    return rt_data


class FmscmdBusiness():

    @classmethod
    def fms_manager(cls, cmdid, keywd=None):
        try:
            if cmdid == 'start':
                return cmd_launch(constr.FMS_START)
            elif cmdid == 'stop':
                return cmd_launch(constr.FMS_STOP)
            else:
                cmd = constr.FMS_ADM_LOAD if cmdid == 'load' else constr.FMS_ADM_UNLOAD
                if keywd is not None:
                    src_keyword = constr.FAULT_PLUGINS_PATH + constr.DEV_SO.get(keywd) + constr.SO_SRC
                    agent_keyword = constr.FAULT_PLUGINS_PATH + constr.DEV_SO.get(keywd) + constr.SO_AGENT
                    cmd_src = "{} {}".format(cmd, src_keyword)
                    cmd_agent = "{} {}".format(cmd, agent_keyword)
                    time.sleep(0.5)
                    modrunninginfo = cls.get_modinfo('running')
                    time.sleep(1)
                    if cmdid == 'load':
                        if "{}\n".format(src_keyword) not in modrunninginfo:
                            time.sleep(1)
                            flag1, rest1 = cmd_launch(cmd_src)
                            # logger.error(str(os.system(cmd_src)))
                            # aa = subprocess.Popen(cmd_src, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            # logger.error("{}  ||  {}".format(str(aa.stdout.readlines()), aa.stderr))
                            if not flag1:
                                logger.error("commands failed :{} {} failed:{}".format(cmd, src_keyword, rest1))
                                return False, constr.FAULT_FAIL
                        if "{}\n".format(agent_keyword) not in modrunninginfo:
                            time.sleep(1)
                            flag2, rest2 = cmd_launch(cmd_agent)
                            # logger.error(str(os.system(cmd_agent)))
                            # logger.error(str(subprocess.Popen(cmd_agent, shell=True, stdout=subprocess.PIPE,
                            #                                   stderr=subprocess.STDOUT)))
                            if not flag2:
                                logger.error("commands failed :{} {} failed:{}".format(cmd, agent_keyword, rest2))
                                return False, constr.FAULT_FAIL
                    else:
                        if "{}\n".format(src_keyword) in modrunninginfo:
                            time.sleep(1)
                            flag1, rest1 = cmd_launch(cmd_src)
                            # logger.error(str(os.system(cmd_src)))
                            if not flag1:
                                logger.error("commands failed :{} {} failed:{}".format(cmd, src_keyword, rest1))
                                return False, constr.FAULT_FAIL
                        if "{}\n".format(agent_keyword) in modrunninginfo:
                            time.sleep(1)
                            flag2, rest2 = cmd_launch(cmd_agent)
                            # logger.error(str(os.system(cmd_agent)))
                            if not flag2:
                                logger.error("commands failed :{} {} failed:{}".format(cmd, agent_keyword, rest2))
                                return False, constr.FAULT_FAIL
                    # flag1, rest1 = cmd_launch(cmd_src)
                    # time.sleep(1)
                    # rest2 = os.system(cmd_agent)
                    # if not flag1:
                    #     return False, constr.FAULT_FAIL
                else:
                    return False, constr.FMS_CMD_ARGS_ERROR
        except Exception, e:
            logger.error("fms_manager cmd:{} error: {}".format(cmdid, str(e.message)))
            return False, str(e.message)
        return True, constr.FAULT_SUCESS

    @classmethod
    def get_modinfo(cls, itemid):
        time.sleep(1)
        if itemid == 'running':
            modinfo = functions.launchcmd(constr.FMS_MODINFO).readlines()
            if modinfo:
                return modinfo[1:]
        elif itemid == 'all':
            mod_list = {}
            modinfo = []
            for dir, subdirs, files in os.walk(constr.FAULT_PLUGINS_PATH):
                for file in files:
                    if file.endswith(".so"):
                        modinfo.append(file)

            running_mod = functions.launchcmd(constr.FMS_MODINFO).readlines()[1:]
            running_list = [x.split(constr.FAULT_PLUGINS_PATH)[-1].replace('\n', '') for x in running_mod]
            for dev in constr.MONITOR_DEV:
                dev_src = "{}{}".format(constr.DEV_SO.get(dev), constr.SO_SRC)
                dev_agent = "{}{}".format(constr.DEV_SO.get(dev), constr.SO_AGENT)
                if dev_src in modinfo and dev_agent in modinfo:
                    mod_list[dev] = False
                    if dev_src in running_list and dev_agent in running_list:
                        mod_list[dev] = True
            return mod_list
        else:
            pass

    @classmethod
    def fault_show(cls, itemid='cpu', **kwargs):
        try:
            if constr.QUERY_CPU == itemid:
                if not (kwargs.get('cpu') and kwargs.get('bank') and kwargs.get('code')):
                    logger.error("fault_show args error: {}".format(str(kwargs)))
                    return False, constr.FAULT_ARGS_ERROR
                return cmd_launch('{}{} {} {} {}'.format(constr.FAULT_SHELL_PATH, constr.FAULT_CPU_SHELL,
                                                         kwargs.get('cpu'),
                                                         kwargs.get('bank'),
                                                         kwargs.get('code')))
            elif constr.QUERY_MEM == itemid:
                if not (kwargs.get('cpu') and kwargs.get('bank') and kwargs.get('address') and kwargs.get('code')):
                    logger.error("fault_show args error: {}".format(str(kwargs)))
                    return False, constr.FAULT_ARGS_ERROR
                return cmd_launch('{}{} {} {} {} {}'.format(constr.FAULT_SHELL_PATH, constr.FAULT_MEM_SHELL,
                                                            kwargs.get('cpu'),
                                                            kwargs.get('bank'),
                                                            kwargs.get('address'),
                                                            kwargs.get('code')))
            elif constr.QUERY_DISK == itemid:
                if not kwargs.get('fault'):
                    logger.error("fault_show args error: {}".format(str(kwargs)))
                    return False, constr.FAULT_ARGS_ERROR
                return cmd_launch('{}{} {}'.format(constr.FAULT_SHELL_PATH, constr.FAULT_DISK_SHELL, kwargs.get('fault')))
            else:
                pass

        except Exception, e:
            logger.error("fault_show error, itemid = {} , error info : {}".format(itemid, str(e.message)))
            return False, constr.FAULT_FAIL

        return None


def cmd_launch(cmdstr):
    code, stout = commands.getstatusoutput(cmdstr)
    if code != 0:
        return False, stout
    return True, stout


# def update_db():
#     cpus = CpuEvents.objects.all()
#     for p in cpus:
#         p.time = "{}-{}-{} {}".format(p.year, p.month, p.day, p.time)
#         p.save()
#     mems = MemEvents.objects.all()
#     for p in mems:
#         p.time = "{}-{}-{} {}".format(p.year, p.month, p.day, p.time)
#         p.save()
#     disks = DiskEvents.objects.all()
#     for p in disks:
#         p.time = "{}-{}-{} {}".format(p.year, p.month, p.day, p.time)
#         p.save()
#     reps = RepEvents.objects.all()
#     for p in reps:
#         p.time = "{}-{}-{} {}".format(p.year, p.month, p.day, p.time)
#         p.save()
class HearthBusiness():

    @classmethod
    def hearth_level(cls):
        """
        读数据表
        :return:
        """
        try:
            dev_hearth = {}
            hearth_level_info = DevStatus.objects.using('faultsetting').all()
            for dev_info in hearth_level_info:
                dev_hearth[strip(dev_info.dev_name)] = strip(dev_info.status)

        except Exception, e:
            logger.error("hearth_level query error: {}".format(str(e)))
            return False, str(e)

        return True, dev_hearth

    @classmethod
    def heart_grade(cls):
        """
        读数据表
        :return:
        """
        try:
            dev_score = {}
            hearth_grade_info = DevScore.objects.using('faultsetting').all()
            for dev_info in hearth_grade_info:
                dev_score[strip(dev_info.dev_name)] = strip(str(dev_info.score))

        except Exception, e:
            logger.error("heart_grade query error: {}".format(str(e)))
            return False, str(e)

        return True, dev_score


class EmailBusiness():

    @classmethod
    def get_emaillist(cls):
        try:
            mail_list = []
            mail_query = Email.objects.using('faultsetting').filter(status='enable')
            for mail in mail_query:
                mail_list.append(mail.email)
        except Exception, e:
            logger.error("get_emaillist error : {}".format(str(e)))
            return False, str(e)
        return True, ';'.join(mail_list)

    @classmethod
    def set_email(cls, mailinfo):
        try:
            rtn_flag = True
            rtn_msg = ''
            if mailinfo:
                # mail_list = kwargs.get('email').encode("utf-8").split(';')
                # logger.error(mailinfo)
                mail_list = mailinfo.split(';')
                # mail_query = Email.objects.using('faultsetting').filter(status='enable')
                for mail in mail_list:
                    # logger.error(mail)
                    mail_check = Email.objects.using('faultsetting').filter(email=strip(mail))
                    # logger.error(mail_check)
                    # for mail_check_temp in mail_check:
                    if not mail:
                        continue
                    if mail_check:
                        # if mail_check_temp is not None:
                        rtn_flag, rtn_msg = False, "email:{} existed;{}".format(strip(mail), rtn_msg)
                        continue
                    Email.objects.using('faultsetting').create(email=strip(mail), status='enable')
                rtn_msg = constr.FAULT_SUCESS if rtn_msg == '' else rtn_msg
            else:
                return False, constr.FAULT_ARGS_ERROR
        except Exception, e:
            logger.error("set_email error : {}".format(str(e)))
            return False, str(e)
        return rtn_flag, rtn_msg

    @classmethod
    def delete_email(cls, itemid):
        try:
            if itemid is not None:
                Email.objects.using('faultsetting').filter(email=itemid).delete()
            else:
                return False, constr.FAULT_ARGS_ERROR
        except Exception, e:
            logger.error("delete_email error : {}".format(str(e)))
            return False, str(e)
        return True, constr.FAULT_SUCESS


class HABusiness():

    @classmethod
    def get_HAinfo(cls):
        try:
            ha_list = []
            if os.path.exists(constr.HA_CONF_FILE):
                with open(constr.HA_CONF_FILE) as ha_conf:
                    for line in ha_conf:
                        if strip(line) and not strip(line).startswith("#"):
                            ha_list.append(strip(line))
                            break
            # ha_query = Ha.objects.using('faultsetting').filter(status='enable')
            # for ha in ha_query:
            #     ha_list.append({'id': ha.id, 'name_node': ha.name_node, 'role': ha.role, 'ip_addr': ha.ip_addr, 'port': ha.port, 'status': ha.status})
        except Exception, e:
            logger.error("get_HAinfo error : {}".format(str(e)))
            return False, str(e)
        return True, ha_list

    @classmethod
    def set_ha(cls, **kwargs):
        try:
            if kwargs is not None and kwargs.get('ip') is not None:
                # Ha.objects.using('faultsetting').create(ip_addr=kwargs.get('ip'), status='enable')
                with open(constr.HA_CONF_FILE, 'w') as ha_conf:
                    ha_conf.writelines(strip(kwargs.get('ip')))
            else:
                return False, constr.FAULT_ARGS_ERROR
        except Exception, e:
            logger.error("set_ha error : {}".format(str(e)))
            return False, str(e)
        return True, constr.FAULT_SUCESS


    @classmethod
    def delete_ha(cls, itemid):
        try:
            if itemid is not None:
                # Ha.objects.using('faultsetting').filter(id=itemid).delete()
                with open(constr.HA_CONF_FILE, 'w') as ha_conf:
                    ha_conf.writelines("")
            else:
                return False, constr.FAULT_ARGS_ERROR
        except Exception, e:
            logger.error("delete_ha error : {}".format(str(e)))
            return False, str(e)
        return True, constr.FAULT_SUCESS
