"""
The main module fore processing the firewall related tasks.
"""
from public import functions

import ksmp.logger as log
import const
import os


__author__ = 'shaomingwu@inspur.com'


class FirewallBusiness():
    """
    1, Apply the modification.
    2, Reset (Flush) firewall protocol items.
    3, Enable or disable firewall service when launching os.
    """
    def __init__(self):
        pass

    @classmethod
    def apply_modification(cls):
        """
        Apply all of the modification.
        :return:
        """
        cmdstr = "/sbin/service iptables save && /sbin/service ip6tables save  \
                 && systemctl start iptables.service && systemctl start ip6tables.service"
        cmdout = functions.launchcmd(cmdstr)

        if cmdout:
            for line in cmdout:
                pass

        return True, const.FW_SUCCEEDED

    @classmethod
    def reset_all(cls):
        """
        Flush all of the firewall protocol items.
        :return:
        iptables --help
          --flush   -F [chain]		Delete all rules in  chain or all chains

        """
        cmdstr = "systemctl stop iptables.service && systemctl stop ip6tables.service \
                  && iptables --flush &&  ip6tables --flush \
                  && /sbin/service iptables save && /sbin/service ip6tables save \
                  && systemctl start iptables.service &&systemctl start ip6tables.service "

        cmdout = functions.launchcmd(cmdstr)

        if cmdout:
            for line in cmdout:
                pass

        return True, const.FW_SUCCEEDED

    @classmethod
    def enable_service(cls, enableflag):
        """
        Enable or disable firewall service according to enableflag.
        :param enableflag:
        :return:
        """
        cmdstr = "systemctl enable iptables.service && systemctl enable ip6tables.service "
        if not enableflag:
            cmdstr = "systemctl disable iptables.service && systemctl disable ip6tables.service"

        cmdout = functions.launchcmd(cmdstr)

        if cmdout:
            for line in cmdout:
                pass

        return True, const.FW_SUCCEEDED


class FirewallManger():
    """
    firewall policy query or manager items
    """
    def firewall_status(self):
        """

        :return:the current firewall status of system
        """
        dynamic_cmd_str = "systemctl is-active firewalld"
        iptables_cmd_str = " systemctl is-active iptables "
        ip6tables_cmd_str = " systemctl is-active ip6tables"
        firewall_mode = 'UNKNOWN'
        if os.popen(dynamic_cmd_str).readline().strip('\n') == 'active':
            firewall_mode = 'DYNAMIC'
        elif os.popen(iptables_cmd_str).readline().strip('\n') == 'active':
            firewall_mode = 'STATIC'
        elif os.popen(ip6tables_cmd_str).readline().strip('\n') == 'active':
            firewall_mode = 'STATIC'
        else:
            firewall_mode = 'UNKNOWN'
        return firewall_mode

    def enable_static_firewall(self):
        cmd = 'systemctl enable iptables.service && systemctl enable ip6tables.service"'
        ip4_enable_stat = os.popen('systemctl is-enabled iptables').readline()
        ip6_enable_stat = os.popen('systemctl is-enabled ip6tables').readline()
        if ip6_enable_stat == 'masked' and ip4_enable_stat == 'masked':
            self.mask_service('firewalld')
            self.unmask_service('ip6tables')
            self.unmask_service('iptables')
        elif ip4_enable_stat == 'disabled' and ip6_enable_stat == 'masked':
            self.mask_service('firewalld')
            self.unmask_service('ip6tables')
        elif ip4_enable_stat == 'masked' and ip6_enable_stat == 'disabled':
            self.mask_service('firewalld')
            self.unmask_service('iptables')
        else:
            self.mask_service('firewalld')
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def start_static_firewall(self):
        """
        start static firewall:iptables,ip6tables
        :return:
        """
        cmd = 'systemctl stop firewalld.service && systemctl start iptables.service \
               && systemctl start ip6tables.service'
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def enable_firewalld(self):
        """
        enable firewalld
        :return:
        """
        cmd = 'systemctl enable firewalld'
        enable_stat = os.popen('systemctl is-enabled firewalld').readline()
        if enable_stat == 'disabled':
            self.mask_service('iptables')
            self.mask_service('ip6tables')
        elif enable_stat == 'masked':
            self.unmask_service('firewalld')
            self.mask_service('iptables')
            self.mask_service('ip6tables')
        else:
            self.mask_service('iptables')
            self.mask_service('ip6tables')
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def start_firewall_service(self, mode):
        """
        Start  firewall service:firewalld,iptables,ip6tables
        :return:
        """
        cmd = ''
        if mode == 'DYNAMIC':
            cmd = 'systemctl start firewalld'
        else:
            cmd = 'systemctl start iptables && systemctl start ip6tables'
            return cmd
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def stop_firewall_service(self, mode):
        """
        Stop the firewall service:firewalld,iptables,ip6tables
        :return:
        """
        cmd = ''
        if mode == 'DYNAMIC':
            cmd = 'systemctl stop firewalld'
        else:
            cmd = 'systemctl stop iptables && systemctl stop ip6tabes'
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def mask_service(self, service_name):
        """
        Mask a service
        :return:
        """
        cmd = 'systemctl mask '+service_name
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def unmask_service(self, service_name):
        """
        Unmask a service
        :return:
        """
        cmd = 'systemctl unmask '+service_name
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            return False

    def get_firewalld_status(self):
        """

        :return: the firewalld status:running or not running
        """
        status_list = ['running', 'not running']
        firewall_status = 1
        cmd = 'firewall-cmd --state'
        result = os.popen(cmd).read().strip('\n')
        if result.find('not running') > -1:
            firewall_status = 0
        elif result == 'running':
            firewall_status = 1
        else:
            firewall_status = -1
            log.error(const.FIREWALLD_NOT_INSTALL)
        return firewall_status

    def get_firewall_panic_mode(self):
        """
        query the system firewall panic mode

        """
        panic_mode = '0'
        cmd = 'firewall-cmd --query-panic && echo "on" || echo "off"'
        result = os.popen(cmd).readlines()
        panic_status = result[1].strip('\n')
        if panic_status != 'off':
            panic_mode = '1'
        panic_mode_dic = {'panic_mode': panic_mode}
        return panic_mode_dic

    def set_panic_mode(self, mode):
        """
        set the system firewall panic mode:on or off
        :return: true or false
        """
        cmd = 'firewall-cmd --panic-'+mode
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            log.error(const.SET_PANIC_MODE_FAILED+mode)
            return False

    def get_support_zones(self, config_type):
        """
        get a list of all support zones
        :param config_type:
        :return:list
        """
        zones_list = []
        firewalld_status = self.get_firewalld_status()
        if firewalld_status != 1:
            return zones_list
        cmd = ''
        if config_type == 'runtime' or config_type == '':
            cmd = 'firewall-cmd --get-zones'
        else:
            cmd = 'firewall-cmd --permanent --get-zones'
        result = os.popen(cmd).readlines()
        for line in result:
            zone_line = line.split()
            for zone in zone_line:
                zones_list.append(zone)
        return zones_list

    def get_active_zones(self):
        """
        get a list of all active zones
        :return:
        """
        active_zones = []
        firewalld_status = self.get_firewalld_status()
        if firewalld_status != 1:
            return active_zones
        cmd = 'firewall-cmd --get-active-zones'
        result = os.popen(cmd).read().split('\n')
        for zone in result[0:(len(result)-1):2]:
            active_zones.append(zone)
        return active_zones

    def get_default_zones(self):
        """
        get a list of all default zones
        :return:list
        """
        default_zone = []
        cmd = 'firewall-cmd --get-default-zone'
        result = os.popen(cmd).read()
        if result:
            default_zone.append(result.strip('\n'))
        return default_zone

    def set_default_zone(self, zone_name):
        """
        set the default zone
        :return: true or false
        """
        cmd = 'firewall-cmd --set-default-zone='+zone_name
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            log.error(const.SET_DEFAULT_ZONE_FAILED+zone_name)
            return False

    def reload_firewall(self, is_complete):
        """
        reload the system firewall
        :param is_complete:
        :return:
        """
        cmd = ''
        if is_complete == 'TRUE':
            cmd = 'firewall-cmd --complete-reload'
        else:
            cmd = 'firewall-cmd --reload'
        result = os.system(cmd)
        if result == 0:
            return True
        else:
            log.error(const.RELOAD_FIREWALL_FAILED)
            return False

    def get_icmp(self, config_type):
        """
        get the support icmp information
        :return:
        """
        icmp_list = []
        cmd = ''
        if config_type == 'permanent':
            cmd = 'firewall-cmd --permanent --get-icmptypes'
        else:
            cmd = 'firewall-cmd --get-icmptypes'
        icmp_list = os.popen(cmd).read().split()
        return icmp_list

    def get_service(self, config_type):
        """
        get a list of all support services
        :param config_type:
        :return:
        """
        service_list = []
        firewalld_status = self.get_firewalld_status()
        if firewalld_status != 1:
            return service_list
        cmd = ''
        if config_type == 'permanent':
            cmd = 'firewall-cmd --permanent --get-services'
        else:
            cmd = 'firewall-cmd --get-services'
        service_list = os.popen(cmd).read().split()

        return service_list

    def get_enabled_service(self, zone_name, service_name, config_type):
        """
        List the enabled services in a zone or query a service in a zone
        :param zone_name:
        :return:
        """
        if service_name == 'all':
            cmd = ''
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --list-services'
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --list-services'
            result = os.popen(cmd).read().split()
            enable_service = {'services': result}
            return enable_service

        else:
            status = {}
            is_enable = '0'
            enable_list = self.get_service(config_type)
            if service_name not in enable_list:
                is_enable = '-1'
                status = {'status': is_enable}
                return status
            cmd = ''
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --query-service=' + service_name
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --query-service=' + service_name
            result = os.popen(cmd).read().strip('\n')
            if result == 'yes':
                is_enable = '1'
            status = {'status': is_enable}

            return status

    def enable_service(self, zone_name, service_name, config_type, timeout):
        """

        :param zone_name:
        :param service_name:
        :param config_type:
        :return:
        """
        if service_name == '':
            return 'service name can not be empty', False
        cmd = ''
        if config_type == 'permanent':
            if zone_name == '':
                if timeout == '':
                    cmd = 'firewall-cmd --permanent --add-service=' + service_name
                else:
                    cmd = 'firewall-cmd --permanent --add-service=' + service_name + ' --timeout=' + timeout
            else:
                if timeout == '':
                    cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --add-service=' + service_name
                else:
                    cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --add-service=' + service_name + \
                          ' --timeout=' + timeout
        else:
            if zone_name == '':
                if timeout == '':
                    cmd = 'firewall-cmd --add-service=' + service_name
                else:
                    cmd = 'firewall-cmd --add-service=' + service_name + \
                          ' --timeout=' + timeout
            else:
                if timeout == '':
                    cmd = 'firewall-cmd --zone=' + zone_name + ' --add-service=' + service_name
                else:
                    cmd = 'firewall-cmd --zone=' + zone_name + ' --add-service=' + service_name + \
                          ' --timeout=' + timeout
        result = os.system(cmd)
        if result == 0:
            return 'enable success', True
        else:
            log.error(const.ENABLE_SERVICE_FAILED+service_name)
            return const.ENABLE_SERVICE_FAILED+service_name, False

    def disable_service(self, zone_name, service_name, config_type):
        """

        :param zone_name:
        :param service_name:
        :param config_type:
        :return:
        """
        services_list = self.get_service(config_type)
        if service_name not in services_list:
            log.error('invalid service name:'+service_name)
            return 'error: invalid service name:'+service_name, False
        cmd = ''
        if config_type == 'permanent':
            if zone_name == '':
                cmd = 'firewall-cmd --permanent --remove-service=' + service_name

            else:
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --remove-service=' + service_name

        else:
            if zone_name == '':
                cmd = 'firewall-cmd --remove-service=' + service_name

            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --remove-service=' + service_name
        result = os.system(cmd)
        if result == 0:
            return 'disable success', True
        else:
            log.error(const.DISABLE_SERVICE_FAILED+service_name)
            return const.DISABLE_SERVICE_FAILED+service_name, False

    def get_ports(self, confit_type, zone_name):
        """
        Get the ports and protocol in a zone
        :param confit_type:
        :param zone_name:
        :return:
        """
        ports = []
        firewalld_status = self.get_firewalld_status()
        if firewalld_status != 1:
            return ports
        cmd = ''
        if zone_name != '':
            if confit_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --list-port'
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --list-port'
        else:
            if confit_type == 'permanent':
                cmd = 'firewall-cmd --permanent --list-port'
            else:
                cmd = 'firewall-cmd --list-port'
        result = os.popen(cmd).read().split()
        ports = []
        ports_dic = {}
        for p in result:
            port = p.split('/')
            port_dict = {
             'port': port[0],
             'protocol': port[1]
            }
            ports.append(port_dict)
        return ports

    def add_port(self, config_type, zone_name, port, protocol):
        """
        Add port and protocol to a zone
        :param config_type:
        :param zone_name:
        :param port:
        :param protocol:
        :return:
        """
        prot = ('udp', 'tcp')
        if self.port_isvalid(port) and protocol in prot:
            log.debug(port)
            port = self.change_type(port)
            cmd = ''
            if zone_name != '':
                if config_type == 'permanent':
                    cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --add-port=' + port + '/' + protocol
                else:
                    cmd = 'firewall-cmd --zone=' + zone_name + ' --add-port=' + port + '/' + protocol
            else:
                if config_type == 'permanent':
                    cmd = 'firewall-cmd --permanent' + ' --add-port=' + port + '/' + protocol
                else:
                    cmd = 'firewall-cmd' + ' --add-port=' + port + '/' + protocol
            result = os.system(cmd)
            if result == 0:
                return 'add port success', True
            else:
                log.error(const.ADD_PORT_FAILED+port+'&'+protocol)
                return 'add port failed', False

        else:
            log.error(const.PORT_OR_PROTOCOL_INVALID+port+'&'+protocol)
            return 'port or protocol is invalid ,please resume load', False

    def remove_port(self, config_type, zone_name, port, protocol):
        """
        Remove port and protocol from a zone
        :param config_type:
        :param zone_name:
        :param port:
        :param protocol:
        :return:
        """
        cmd = ''
        if zone_name != '':
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --remove-port=' + port + '/' + protocol
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --remove-port=' + port + '/' + protocol
        else:
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent' + ' --remove-port=' + port + '/' + protocol
            else:
                cmd = 'firewall-cmd' + ' --remove-port=' + port + '/' + protocol
        result = os.system(cmd)
        if result == 0:
            return 'remove port success', True
        else:
            log.error(const.REMOVE_PORT_FAILED+port+'&'+protocol)
            return 'remove port failed', False

    def port_isvalid(self, port):
        """

        :param port:
        :return:
        """
        in_port = port.split('-')
        if len(in_port) == 1:
            if in_port[0].isdigit():
                return True
            else:
                return False
        elif len(in_port) == 2:
            if in_port[0].isdigit() and in_port[1].isdigit():
                if int(in_port[0]) < int(in_port[1]):
                    return True
                else:
                    return False
        else:
            return False

    def get_interface(self, config_type, zone_name):
        """
        Get all interfaces in a zone
        :param config_type:
        :param zone_name:
        :return:
        """
        result = []
        firewalld_status = self .get_firewalld_status()
        if firewalld_status != 1:
            return result
        cmd = ''
        if zone_name != '':
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --list-interfaces'
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --list-interfaces'
        else:
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --list-interfaces'
            else:
                cmd = 'firewall-cmd --list-interfaces'
        result = os.popen(cmd).read().split()
        return result

    def add_interface(self, config_type, zone_name, interface):
        """
        Add a interface to a zone
        :param config_type:
        :param zone_name:
        :param interface:
        :return:
        """
        if interface == '' or interface == ' ':
            log.error('interface is invalid:'+interface)
            return 'interface is invalid', False
        cmd = ''
        if zone_name != '':
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --add-interface=' + interface
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --add-interface=' + interface
        else:
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent' + ' --add-interface=' + interface
            else:
                cmd = 'firewall-cmd' + ' --add-interface=' + interface
        result = os.system(cmd)
        if result == 0:
            return 'add interface success', True
        else:
            log.error(const.ADD_INTERFACE_FAILED+interface)
            return 'add interface failed', False

    def remove_interface(self, config_type, zone_name, interface):
        """
        Remove a interface from a zone
        :param config_type:
        :param zone_name:
        :param interface:
        :return:
        """
        if interface == '' or interface == ' ':
            log.error('interface is invalid:'+interface)
            return 'interface is invalid', False
        cmd = ''
        if zone_name != '':
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --remove-interface=' + interface
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --remove-interface=' + interface
        else:
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent' + ' --remove-interface=' + interface
            else:
                cmd = 'firewall-cmd' + ' --remove-interface=' + interface
        result = os.system(cmd)
        if result == 0:
            return 'remove interface success', True
        else:
            log.error(const.REMOVE_INTERFACE_FAILED+interface)
            return 'remove interface failed', False

    def change_interface_zone(self, config_type, zone_name, interface):
        """
        Change the zone an interface belongs to
        :param config_type:
        :param zone_name:
        :param interface:
        :return:
        """
        if interface == '' or interface == ' ':
            log.error('interface is invalid:'+interface)
            return 'interface is invalid', False
        if zone_name != '':
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent --zone=' + zone_name + ' --change-interface=' + interface
            else:
                cmd = 'firewall-cmd --zone=' + zone_name + ' --change-interface=' + interface
        else:
            if config_type == 'permanent':
                cmd = 'firewall-cmd --permanent' + ' --change-interface=' + interface
            else:
                cmd = 'firewall-cmd' + ' --change-interface=' + interface
        result = os.system(cmd)
        if result == 0:
            return 'change the zone an interface belongs to success', True
        else:
            log.error(const.CHANGE_INTERFACE_FAILED+interface+'&'+zone_name)
            return const.CHANGE_INTERFACE_FAILED+interface+'&'+zone_name, False

    def get_configuration(self, config_type):
        """
        Get the configuration info of runtime or permanent
        :param config_type:
        :return:
        """
        result = {}

        zone_list = self.get_support_zones(config_type)
        zone_config = []
        # zone_dic = {}
        for zone in zone_list:
            enabled_services = self.get_enabled_service(zone, 'all', config_type)
            ports = self.get_ports(config_type, zone)
            interfaces = self.get_interface(config_type, zone)
            conf_dic = {
                'enabled_service': enabled_services,
                'ports': ports,
                'interface': interfaces
            }
            zone_dic = {
                'zone_name': zone,
                'config_info': conf_dic
            }
            zone_config.append(zone_dic)
        service_list = self.get_service(config_type)
        active_zones = self.get_active_zones()
        result = {
            'zone_configuration': zone_config,
            'service': service_list,
            'active_zones': active_zones
        }
        return result

    def change_type(self, var):

        val_list = var.split('-')
        if len(val_list) == 1:
            log.debug(str(int(val_list[0])))
            return str(int(val_list[0]))
        else:
            return str(int(val_list[0])) + '-' + str(int(val_list[1]))
