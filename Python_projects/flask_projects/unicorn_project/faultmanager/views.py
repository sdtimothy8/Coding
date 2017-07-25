# coding:utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from faultmanager.business import CountBusiness, EventsDetailBusiness, FaultsBusiness, FmscmdBusiness, HearthBusiness
from faultmanager.business import EmailBusiness, HABusiness
from faultmanager import constr
# Create your views here.
__author__ = 'zhuysh@inspur.com'


class EventList(APIView):

    def get(self, request, itemid):

        args = {}
        today = datetime.date.today()
        args[constr.END_TIME] = str(today)
        if request.GET.get(constr.QUERY_CYCLE):
            args[constr.START_TIME] = str(today - datetime.timedelta(days=int(request.GET.get(constr.QUERY_CYCLE)) - 1))
        else:
            args[constr.START_TIME] = str(today - datetime.timedelta(days=6))

        if request.GET.get(constr.START_TIME):
            args[constr.START_TIME] = request.GET.get(constr.START_TIME)
        if request.GET.get(constr.END_TIME):
            args[constr.END_TIME] = request.GET.get(constr.END_TIME)

        flag, evt_count = CountBusiness.evt_count(qtype=itemid, **args)

        if flag:
            return Response({"events": evt_count}, status=status.HTTP_200_OK)
        else:
            return Response({"events": ""}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDetailList(APIView):

    def get(self, request, itemid):

        args = {}
        today = datetime.date.today()
        args[constr.END_TIME] = str(today)
        if request.GET.get(constr.QUERY_CYCLE):
            args[constr.START_TIME] = str(today - datetime.timedelta(days=int(request.GET.get(constr.QUERY_CYCLE)) - 1))
        else:
            args[constr.START_TIME] = str(today - datetime.timedelta(days=6))

        if request.GET.get(constr.START_TIME):
            args[constr.START_TIME] = request.GET.get(constr.START_TIME)
        if request.GET.get(constr.END_TIME):
            args[constr.END_TIME] = request.GET.get(constr.END_TIME)
        if request.GET.get(constr.QUERY_DEV):
            args[constr.QUERY_DEV] = request.GET.get(constr.QUERY_DEV)

        flag, evt_rt = EventsDetailBusiness.evt_detail(qtype=itemid, **args)

        if flag:
            return Response({"events_detail": evt_rt}, status=status.HTTP_200_OK)
        else:
            return Response({"events_detail": evt_rt}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaultsManager(APIView):

    def get(self, request, itemid):

        rt_value = None
        if itemid in constr.MONITOR_DEV:
            rt_value = FaultsBusiness.read_esc(itemid)
        elif itemid in constr.DEV_SRC:
            rt_value = FaultsBusiness.operate_src(filename=itemid)
        elif itemid == 'status':
            rt_value = FaultsBusiness.fmd_status()

        if rt_value:
            return Response(rt_value, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, itemid):
        flag = None
        if itemid in constr.MONITOR_DEV:
            rule_data = request.data.get("rule")
            if rule_data:
                flag = FaultsBusiness.modify_agent(filename=itemid, data=rule_data)
        else:
            time_data = request.data.get("data")
            if time_data:
                flag = FaultsBusiness.operate_src(filename=itemid, otype='write', sdata=time_data)

        if flag:
            return Response({"result": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FmsManagerType(APIView):

    def get(self, request, itemid, otype):
        rtnvalue = FaultsBusiness.fmtype_query(itemid)
        if rtnvalue:
            return Response(rtnvalue, status=status.HTTP_200_OK)
        else:
            return Response({"result": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, itemid, otype):

        file_data = {}
        if 'manual' == otype:
            file_data['fname'] = request.data['fileName']
            file_data['fdata'] = request.FILES['file']

        flag, rtstring = FaultsBusiness.fmtype_manager(itemid, otype, **file_data)
        if flag:
            return Response({"result": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": rtstring}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FmscmdManager(APIView):

    def get(self, requst, itemid):

        modinfo = FmscmdBusiness.get_modinfo(itemid)

        if modinfo:
            return Response({"modinfo": modinfo}, status=status.HTTP_200_OK)
        else:
            return Response({"modinfo": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, itemid):
        mod = request.data.get("mod")
        flag, rtmsg = FmscmdBusiness.fms_manager(itemid, mod)
        if flag:
            return Response({"result": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": rtmsg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaultsMonitor(APIView):

    def get(self, request):
        """
        :param request:
        :return:
        """
        args = {}
        today = datetime.date.today()
        args[constr.END_TIME] = str(today)
        if request.GET.get(constr.QUERY_CYCLE):
            args[constr.START_TIME] = str(today - datetime.timedelta(days=int(request.GET.get(constr.QUERY_CYCLE)) - 1))
        else:
            args[constr.START_TIME] = str(today - datetime.timedelta(days=6))

        if request.GET.get(constr.START_TIME):
            args[constr.START_TIME] = request.GET.get(constr.START_TIME)
        if request.GET.get(constr.END_TIME):
            args[constr.END_TIME] = request.GET.get(constr.END_TIME)

        flag, rtn_info = FaultsBusiness.monitor_status(**args)
        if flag:
            return Response({"monitorstatus": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({"monitorstatus": rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DevCount(APIView):

    def get(self, request, itemid):

        args = {}
        today = datetime.date.today()
        args[constr.END_TIME] = str(today)
        if request.GET.get(constr.QUERY_CYCLE):
            args[constr.START_TIME] = str(today - datetime.timedelta(days=int(request.GET.get(constr.QUERY_CYCLE)) - 1))
        else:
            args[constr.START_TIME] = str(today - datetime.timedelta(days=6))

        if request.GET.get(constr.START_TIME):
            args[constr.START_TIME] = request.GET.get(constr.START_TIME)
        if request.GET.get(constr.END_TIME):
            args[constr.END_TIME] = request.GET.get(constr.END_TIME)

        flag, rtn_info = CountBusiness.dev_count(itemid, **args)
        if flag:
            return Response({"counts": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({"counts": rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaultDetail(APIView):

    def get(self, request, itemid):

        flag, rtn_info = EventsDetailBusiness.fualt_detail(itemid)
        if flag:
            return Response({"detail": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaultShow(APIView):

    def get(self, request, itemid):
        return Response({"detail": []}, status=status.HTTP_200_OK)

    def post(self, request, itemid):
        data = request.data.get("args")
        flag, rtn_info = FmscmdBusiness.fault_show(itemid, **data)
        if flag:
            return Response({"detail": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaultHealth(APIView):

    def get(self, request, itemid):

        if itemid == 'level':
            flag, rtvalue = HearthBusiness.hearth_level()
        else:
            flag, rtvalue = HearthBusiness.heart_grade()

        if flag:
            return Response(rtvalue, status=status.HTTP_200_OK)
        else:
            return Response(rtvalue, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailSetting(APIView):

    def get(self, request, itemid):

        flag, rtn_info = EmailBusiness.get_emaillist()
        if flag:
            return Response({"email": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, itemid):
        mailinfo = request.data.get('email')
        flag, rtn_info = EmailBusiness.set_email(mailinfo)
        if flag:
            return Response(rtn_info, status=status.HTTP_200_OK)
        else:
            return Response(rtn_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, itemid):
        flag, rtn_info = EmailBusiness.delete_email(itemid)
        if flag:
            return Response(rtn_info, status=status.HTTP_200_OK)
        else:
            return Response(rtn_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HaSetting(APIView):

    def get(self, request, itemid):

        flag, rtn_info = HABusiness.get_HAinfo()
        if flag:
            return Response({"halist": rtn_info}, status=status.HTTP_200_OK)
        else:
            return Response({rtn_info}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, itemid):
        hainfo = request.data.get('ip')
        flag, rtn_info = HABusiness.set_ha(**{'ip': hainfo})
        if flag:
            return Response(rtn_info, status=status.HTTP_200_OK)
        else:
            return Response(rtn_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, itemid):
        flag, rtn_info = HABusiness.delete_ha(itemid)
        if flag:
            return Response(rtn_info, status=status.HTTP_200_OK)
        else:
            return Response(rtn_info, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
