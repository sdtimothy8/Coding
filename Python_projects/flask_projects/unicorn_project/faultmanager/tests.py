from django.test import TestCase
import mock
from mock import patch
from faultmanager import business

__author__ = 'zhuysh@inspur.com'

# Create your tests here.


class TestEventList(TestCase):

    @mock.patch('business.time_count')
    @mock.patch('business.__format_evt_counts')
    def test_evt_count(self, format_mock, time_count_mock):
        format_mock.return_value = {}
        time_count_mock.return_value = {}
        ref = business.CountBusiness()
        time = {'start': '2016-05-11', 'end': '2016-05-18'}
        flag, rtn = ref.evt_count('evt', time)
        self.assertEquals(flag, True)
        self.assertEquals(rtn, {})

        flag2, rtn2 = ref.evt_count('dev', time)
        self.assertEquals(flag2, True)
        self.assertEquals(rtn2, {})

        flag3, rtn3 = ref.evt_count('cpu', time)
        self.assertEquals(flag3, True)
        self.assertEquals(rtn3, {})

    def test_dev_count(self):
        ref = business.CountBusiness()
        time = {'start': '2016-05-11', 'end': '2016-05-18'}
        flag, rtn = ref.dev_count('cpu', time)

        self.assertEquals(flag, True)

        flag2, rtn2 = ref.dev_count('', time)

        self.assertEquals(flag2, False)


class TestEventsDetailBusiness(TestCase):

    def test_evt_detail(self):
        ref = business.EventsDetailBusiness()
        time = {'start': '2016-05-11', 'end': '2016-05-18'}
        flag, rtn = ref.evt_detail('recent', time)

        self.assertEquals(flag, True)

        flag2, rtn2 = ref.evt_detail('repair', time)

        self.assertEquals(flag2, True)

        flag3, rtn3 = ref.evt_detail('evtlist', {'start': '2016-05-11', 'end': '2016-05-18', 'dev': 'cpu'})

        self.assertEquals(flag3, True)

        flag4, rtn4 = ref.evt_detail('devrecent', {'start': '2016-05-11', 'end': '2016-05-18', 'dev': 'cpu'})

        self.assertEquals(flag4, True)

    def test_fualt_detail(self):
        ref = business.EventsDetailBusiness()
        faultid = 'ereport.cpu.unclassified_ce'

        flag, rtn = ref.fualt_detail(faultid)

        self.assertEquals(flag, True)


class TestFaultsBusiness(TestCase):

    def test_read_esc(self):
        ref = business.FaultsBusiness()
        rtn = ref.read_esc()

        self.assertNotEqual(rtn, False)

    @mock.patch('business.functions.launchcmd')
    @patch('__builtin__.open')
    def test_operate_src(self, open_mock, launchcmd_mock):
        ref = business.FaultsBusiness()
        open_mock.return_value = ['interval 3']

        rtn = ref.operate_src()

        self.assertEquals(rtn, '3')

        launchcmd_mock.return_value = ['interval 3']
        open_mock = open('thefile', 'w+')
        rtn = ref.operate_src('srccpu', 'write', 5)

        self.assertEquals(rtn, True)

    @mock.patch('business.functions.launchcmd')
    def test_fmd_status(self, launchcmd_mock):
        ref = business.FaultsBusiness()
        launchcmd_mock.return_value = ['active']
        flag, rtn = ref.fmd_status()

        self.assertEquals(flag, True)

    def test_fmtype_query(self):
        ref = business.FaultsBusiness()
        rtn = ref.fmtype_query()

        self.assertNotEquals(rtn, False)


class TestFmscmdBusiness(TestCase):

    @mock('business.cmd_launch')
    def test_fms_manager(self, cmd_mock):
        ref = business.FmscmdBusiness()
        cmd_mock.return_value = True, 'sucess'
        flag, rtn = ref.fms_manager('start')

        self.assertEquals(flag, True)

        flag, rtn = ref.fms_manager('stop')

        self.assertEquals(flag, True)

    def test_get_modinfo(self):
        ref = business.FmscmdBusiness()
        rtn = ref.get_modinfo('all')

        self.assertNotEquals(rtn, False)

        rtn = ref.get_modinfo('running')

        self.assertNotEquals(rtn, False)
