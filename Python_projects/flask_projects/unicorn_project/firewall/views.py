"""
The module for firewall related features.
"""
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from business import FirewallManger
from firewall import business
# import move.process_move_rule
from move import process_move_rule
import const

__author__ = 'shaomingwu@inspur.com'


class FirewallList(APIView):
    """
    List all firewall items, or create a new one.
    ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """

    def get(self, request, format=None):
        """
        Get firewall list.
        """
        # Add your code here.
        table_type = request.GET.get('table', '')
        firewall_list = {'firewalls': []}
        if table_type == '' or table_type == 'filter':
            filter_table = os.popen('iptables -L --line-numbers')
            all_chain = get_chains(filter_table)
            firewall_list['firewalls'] = get_rules(all_chain, table_type)
        elif table_type == 'nat':
            nat = os.popen('iptables -t nat -L --line-numbers')
            all_chain = get_chains(nat)
            firewall_list['firewalls'] = get_rules(all_chain, table_type)
        elif table_type == 'mangle':
            mangle = os.popen('iptables -t mangle -L --line-numbers')
            all_chain = get_chains(mangle)
            firewall_list['firewalls'] = get_rules(all_chain, table_type)
        elif table_type == 'raw':
            raw = os.popen('iptables -t raw -L --line-numbers')
            all_chain = get_chains(raw)
            firewall_list['firewalls'] = get_rules(all_chain, table_type)

        return Response(firewall_list, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        1,Append one new firewall protocol item.
        """
        add_data = request.data
        cmd = add_data.get('cmd')
        if cmd.find('iptables -A ') == 0 and cmd.find(';') == -1:
            result = os.system(cmd)
            if result == 0:
                return Response("Add firewall rule success!", status=status.HTTP_200_OK)
            else:
                return Response("Add firewall rule failed! ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("Input command is error! please  use 'iptables --help'", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Update the firewall protocol items.
        1, Apply all of the modification.
        2, Enable or disable firewall service when launching OS.
        """
        # logging.debug("Get for post:")
        # logging.debug(repr(request.data))

        retflg = False
        retstr = const.FW_UNKNOWN_CMD

        commandstr = request.data.get("command", "UNKNOWN")
        if commandstr == "APPLY":
            retflg, retstr = business.FirewallBusiness.apply_modification()
        elif commandstr == "RESET":
            retflg, retstr = business.FirewallBusiness.reset_all()
        elif commandstr == "ENABLESERVICE":
            enableflag = request.data.get("enableflag", "Yes")
            if enableflag.upper() == "YES":
                retflg, retstr = business.FirewallBusiness.enable_service(True)
            else:
                retflg, retstr = business.FirewallBusiness.enable_service(False)
        else:
            pass

        # logging.debug("[%d]%s"%(retflg, retstr))

        if retflg:
            return Response(retstr, status=status.HTTP_200_OK)
        else:
            return Response(retstr, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        """
        Reset the firewall protocol items.
        """
        # logging.debug("Get for post:")
        # logging.debug(repr(request.data))

        table_type = request.data.get('table', None)
        chain_name = request.data.get('chain', None)
        number = request.data.get('number', None)
        result = 0
        if table_type is None or table_type == 'filter':
            if number is not None and chain_name is not None:
                cmd = 'iptables -D '+chain_name+' '+number
                result = os.system(cmd)
        else:
            if chain_name is not None and number is not None:
                    cmd = 'iptables -t '+table_type+' -D '+chain_name+' '+number
                    result = os.system(cmd)
        if result == 0:
            return Response('Delete success!', status=status.HTTP_200_OK)
        else:
            return Response('Delete failed!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FirewallDetail(APIView):
    """
    Provide the methods for processing one firewall item.
    Get , add, update, or delete one item.
    """

    def get(self, request, itemid, format=None):
        """
        Get firewall detail item.
        """
        # Organize your result string here.
        retstr = "FirewallDetail_get. [%s]" % itemid  # Here is just an example.
        return Response(retstr, status=status.HTTP_200_OK)

    def post(self, request, itemid, format=None):
        """
        1,Create one new firewall item.
        """
        # Organize your result string here.
        retstr = "FirewallDetail_post. [%s]" % itemid  # Here is just an example.
        return Response(retstr, status=status.HTTP_200_OK)

    def put(self, request, itemid, format=None):
        """
        1, Update the content for one firewall item: movement.
        2, Apply one firewall item.
        """
        # Organize your result string here.
        retstr = "FirewallDetail_put. [%s]" % itemid  # Here is just an example.
        return Response(retstr, status=status.HTTP_200_OK)

    def delete(self, request, itemid, format=None):
        """
        1,Delete selected firewall item.
        """
        # Organize your result string here.
        retstr = "FirewallDetail_delete. [%s]" % itemid  # Here is just an example.
        return Response(retstr, status=status.HTTP_200_OK)


class FirewallMove(APIView):
    '''
    provide post method as RESTful webservice for moving iptable rules
    '''

    def post(self, request, format=None):
        '''
        post method for moving iptables rules
        param -- request including DATA property
        the 'table', 'chain' and 'newserial' is needed in request.DATA
        return code Response with message and status
        '''
        data = request.DATA
        table = data["table"]
        chain = data["chain"]
        newserial = data["newserial"]

        if len(newserial) <= 1:
            solution = "success"
            message = "nothing to treat."
            return Response(
                {"status": solution, "message": message, "data": data, "order": newserial},
                status=status.HTTP_200_OK)

        for i in range(len(newserial)):
            newserial[i] = int(newserial[i])

        retcode = process_move_rule(table, chain, newserial)
        solution = ''

        if retcode == 0:
            solution = "success"
            message = "move succeed"
        elif retcode == -1:
            solution = "error"
            message = "move wrong"
        else:
            solution = "fail"
            message = "move fail"
        return Response(
            {"status": solution, "message": message, "table": table, "chain": chain, "order": newserial},
            status=status.HTTP_200_OK)


def get_chains(content):
    """
    Get all chains of table
    :param content:
    :return:
    """
    rule_list = []
    for line in content:
        if line.find('Chain ') >= 0:
            ss = line[6:]
            pos = ss.index('(')
            rule_list.append(ss[0:pos])
    return rule_list


def get_rules(chains, table):
    """
    Get the all rules of a table
    :param chains:
    :param table:
    :return:
    """
    all_list = []
    for chain in chains:
        cmd = ''
        if table != '':
            cmd = 'iptables -t '+table+' -L '+chain+' --line-numbers'
        else:
            cmd = 'iptables -L '+chain+' --line-numbers'
        rule_lines = os.popen(cmd).readlines()
        rule_list = []
        if len(rule_lines) >= 3:
            for rule in rule_lines[2: len(rule_lines)]:
                num_line = rule.split()
                rule_string = rule[5: len(rule)]
                rule_dict = {'number': num_line[0], 'rule': rule_string.strip('\n')}
                rule_list.append(rule_dict)
            rules_dict = {'chainName': chain, 'rules': rule_list}
            all_list.append(rules_dict)
    return all_list


class FirewallStatusList(APIView):
    """
    List the dynamic firewall items or configuration
    """
    def get(self, request, format=None):

        fm = FirewallManger()
        firewall_status = fm.get_firewalld_status()
        state = {'status': firewall_status}
        if firewall_status == -1:
            return Response(state, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(state, status=status.HTTP_200_OK)


class FirewalldManager(APIView):
    """
    The system firewall manager
    """

    def get(self, request, format=None):
        """
        the firewall policy query
        """
        fm = FirewallManger()
        fire_mode = FirewallManger.firewall_status(fm)
        return Response(fire_mode, status=status.HTTP_200_OK)

    def put(self, request, format=None):

        """
        config the firewall mode ex:STATIC,DYNAMIC
        """
        cfm = FirewallManger()
        _firemode_list = ['STATIC', 'DYNAMIC', 'UNKNOWN']
        current_mode = cfm.firewall_status()
        _fm = request.data.get('policy')
        if _fm not in _firemode_list:
            return Response('FIREWALL MODE IS INVALID', status=status.HTTP_400_BAD_REQUEST)
        elif current_mode == _fm:
            return Response('FIREWALL MODE IS RUNNING', status=status.HTTP_400_BAD_REQUEST)
        else:
            if current_mode == 'UNKNOWN':
                if _fm == 'STATIC':
                    q1 = cfm.enable_static_firewall()
                    q2 = cfm.start_firewall_service("STATIC")
                    return Response(q2, status=status.HTTP_200_OK)
                else:
                    cfm.enable_firewalld()
                    cfm.start_firewall_service("DYNAMIC")
            else:
                if _fm == 'STATIC':
                    cfm.enable_static_firewall()
                    cfm.stop_firewall_service("DYNAMIC")
                    cfm.start_firewall_service("STATIC")
                else:
                    cfm.enable_firewalld()
                    cfm.stop_firewall_service("STATIC")
                    cfm.start_firewall_service("DYNAMIC")
            return Response('CONFIG SUCCESS', status=status.HTTP_200_OK)


class FirewalldPnaicMode(APIView):
    """
    Dynamic firewall configuration: runtime and permanent
    """
    def get(self, request, format=None):
        """
        query the system firewall panic mode

        """
        fm = FirewallManger()
        panic_mode = fm.get_firewall_panic_mode()
        return Response(panic_mode, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        """

       config the firewall panic mode:on or off
        """
        fm = FirewallManger()
        mode = request.DATA.get('panic_mode')
        mode_struct = ['on', 'off']
        if mode not in mode_struct:
            return Response('Arguments is not invalid!')
        else:
            result = fm.set_panic_mode(mode)
            if result:
                return Response("Config Success!", status=status.HTTP_200_OK)
            else:
                return Response("Config failed!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FirewallZoneList(APIView):
    """
    The system firewall zones manager list
    """
    def get(self, request, format=None):
        """
        get a list if all support zones
        """
        config_type = request.GET.get('config_type', '')
        fm = FirewallManger()
        zone_list = fm.get_support_zones(config_type)
        zones_dic = {'zones': zone_list}
        return Response(zones_dic, status=status.HTTP_200_OK)


class FirewallActiveZones(APIView):
    """
    The System firewall active zones
    """
    def get(self, request, format=None):
        """

        Get a list of all active zones
        """
        fm = FirewallManger()
        active_list = fm.get_active_zones()
        zones_dic = {'zones': active_list}
        return Response(zones_dic, status=status.HTTP_200_OK)


class FirewallDefaultZones(APIView):
    """
    The system firewall default zones
    """
    def get(self, request, format=None):
        """
        Get a list of all default zones.
        """
        fm = FirewallManger()
        default_zone = fm.get_default_zones()[0]
        default = {'default_zones': default_zone}
        if default_zone:
            return Response(default, status=status.HTTP_200_OK)
        else:
            return Response("No default zone in system firewall!", status=status.HTTP_200_OK)

    def put(self, request, format=None):
        """
        set default zone of system firewall

        """
        zone_name = request.data.get('zone_name')
        fm = FirewallManger()
        zone_list = fm.get_support_zones('')
        # if zone_list and zone_name in zone_list:
        result = fm.set_default_zone(zone_name)
        if result:
            return Response('Set default zone success !', status=status.HTTP_200_OK)
        else:
            return Response('Set default zone failed !', status=status.HTTP_400_BAD_REQUEST)
        # else:
            # return Response('This zone is not support for system!', status=status.HTTP_400_BAD_REQUEST)


class FirewallReload(APIView):
    """
    Reload the systems firewall
    """
    def put(self, request, format=None):
        """

        Reload the firewall
        """
        is_complete = request.data.get('complete').upper()
        fm = FirewallManger()
        result = fm.reload_firewall(is_complete)
        if result:
            return Response('Reload success!', status=status.HTTP_200_OK)
        else:
            return Response('Reload failed!', status=status.HTTP_400_BAD_REQUEST)


class FirewallICMP(APIView):
    """
    Get a list of support ICMP
    """
    def get(self, request, format=None):
        """

        Get the ICMP
        """
        icmp_list = []
        config_type = request.GET.get('config_type')
        fm = FirewallManger()
        icmp_list = fm.get_icmp(config_type)
        if icmp_list:
            return Response(icmp_list, status=status.HTTP_200_OK)
        else:
            return Response('The ICMP list is empty!')


class FirewallService(APIView):
    """
    System firewall service manager
    """
    def get(self, request, format=None):
        """
        Get a list of all support services
        """
        fm = FirewallManger()
        config_type = request.GET.get('config_type', '')
        services_list = fm.get_service(config_type)
        services_dic = {'services': services_list}
        return Response(services_dic, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """

        Enable a service of a zone
        """
        config_type = request.DATA.get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        service_name = request.DATA.get('service_name', '')
        timeout = request.DATA.get('timeout', '')
        fm = FirewallManger()
        message, flag = fm.enable_service(zone_name, service_name, config_type, timeout)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """

        Disable a service of a zone
        """
        config_type = request.DATA.get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        service_name = request.DATA.get('service_name', '')
        fm = FirewallManger()
        message, flag = fm.disable_service(zone_name, service_name, config_type)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class FirewallEnableService(APIView):
    """
     List the enabled services in a zone
     OR
     Query a enabled service in a zone
    """
    def get(self, request, format=None):
        """
        Get a list of enabled services or query a enabled service in a zone
        """
        config_type = request.GET.get('config_type', '')
        zone_name = request.GET.get('zone_name', '')
        service_name = request.GET.get('service_name')
        if zone_name == '' or service_name == '':
            return Response('the service name or zone name can not be empty', status=status.HTTP_400_BAD_REQUEST)
        fm = FirewallManger()
        result = fm.get_enabled_service(zone_name, service_name, config_type)
        return Response(result, status=status.HTTP_200_OK)


class FirewallPorts(APIView):
    """
    List ports and protocol in a zone
    """
    def get(self, request, format=None):
        """
        Get the ports and protocol in a zone
        """
        config_type = request.GET.get('config_type', '')
        zone_name = request.GET.get('zone_name', '')
        fm = FirewallManger()
        result = fm.get_ports(config_type, zone_name)
        ports_dic = {'ports': result}
        return Response(ports_dic, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Add protocol in a zone
        """
        config_type = request.DATA .get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        port = request.DATA.get('ports', '')
        protocol = request.DATA.get('protocol', '')
        fm = FirewallManger()
        # return Response(config_type+zone_name+protocol+port)
        message, flag = fm.add_port(config_type, zone_name, port, protocol)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        """
        Delete port from a zone
        """
        config_type = request.DATA.get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        port = request.DATA.get('ports', '')
        protocol = request.DATA.get('protocol', '')
        if port == '' or protocol == '':
            return Response('port or protocol is not empty', status=status.HTTP_400_BAD_REQUEST)
        fm = FirewallManger()
        message, flag = fm.remove_port(config_type, zone_name, port, protocol)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class FirewallInterface(APIView):
    """
    List the interfaces in a zone
    """
    def get(self, request, format=None):
        """
        Get the interfaces in a zone
        """
        config_type = request.GET.get("config_type", '')
        zone_name = request.GET.get("zone_name", '')
        fm = FirewallManger()
        interface_list = fm.get_interface(config_type, zone_name)
        intface_dict = {'interfaces': interface_list}
        return Response(intface_dict, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        """
        Delete an interface from a zone
        """
        config_type = request.DATA .get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        interface = request.DATA.get('interface', '')
        fm = FirewallManger()
        message, flag = fm.remove_interface(config_type, zone_name, interface)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        """
        Add the interface form a zone
        """
        config_type = request.DATA .get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        interface = request.DATA.get('interface', '')
        fm = FirewallManger()
        message, flag = fm.add_interface(config_type, zone_name, interface)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=None):
        """
        Change the zone an interface belongs to
        """
        config_type = request.DATA .get('config_type', '')
        zone_name = request.DATA.get('zone_name', '')
        interface = request.DATA.get('interface', '')
        fm = FirewallManger()
        message, flag = fm.change_interface_zone(config_type, zone_name, interface)
        if flag:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class FirewallConfigType(APIView):
    """
    Chang the config type of the system firewall
    """
    def get(self, request, format=None):
        """

        List the configuration info of the runtime or permanent
        """
        config_type = request.GET.get("config_type", '')
        fm = FirewallManger()
        result = fm.get_configuration(config_type)
        return Response(result, status=status.HTTP_200_OK)
