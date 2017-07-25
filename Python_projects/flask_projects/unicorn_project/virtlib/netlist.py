# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#
# Copyright (C) 2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
#

import logging

import virtinst
# from . import uiutil


class vmmNetworkList(object):
    def __init__(self, conn):
        self.conn = conn
        #
        self._warn_list = None
        self._network_model = None
        self._selected_network = None
        self._netbridge_name = None
        self._net_source_mode_model = None
        self._selected_net_source_mode = None
        self._net_portgroup_model = None
        self._selected_net_portgroup = None
        #
        self._vport_type = None
        self._vport_managerid = None
        self._vport_typeid = None
        self._vport_idver = None
        self._vport_instid = None
        self._init()

    def _cleanup(self):
        try:
            self.conn.disconnect_by_func(self._repopulate_network_list)
            self.conn.disconnect_by_func(self._repopulate_network_list)
            self.conn.disconnect_by_func(self._repopulate_network_list)
            self.conn.disconnect_by_func(self._repopulate_network_list)
        except:
            pass

        self.conn = None


    ##########################
    # Initialization methods #
    ##########################
    def _init(self):
        self._warn_list = []
        self._init_network_model()
        self._init_net_portgroup_model()

    def _init_network_model(self):
        self._network_model = []

    def _init_net_portgroup_model(self):
        self._net_portgroup_model = []
    
    def _get_network_model(self):
        return self._network_model
    
    def _get_net_portgroup_model(self):
        return self._net_portgroup_model

    def _add_warn(self, warn):
        self._warn_list.append(warn)

    def _pretty_network_desc(self, nettype, source=None, netobj=None):
        if nettype == virtinst.VirtualNetworkInterface.TYPE_USER:
            return _("Usermode networking")

        extra = None
        if nettype == virtinst.VirtualNetworkInterface.TYPE_BRIDGE:
            ret = _("Bridge")
        elif nettype == virtinst.VirtualNetworkInterface.TYPE_VIRTUAL:
            ret = _("Virtual network")
            if netobj:
                extra = ": %s" % netobj.pretty_forward_mode()
        else:
            ret = nettype.capitalize()

        if source:
            ret += " '%s'" % source
        if extra:
            ret += " %s" % extra

        return ret

    def _build_source_row(self, nettype, source_name,
        label, is_sensitive, is_running, manual_bridge=False, key=None):
        return [nettype, source_name, label,
                is_sensitive, is_running, manual_bridge,
                key]

    def _find_virtual_networks(self):
        rows = []
        vnet_bridges = []
        default_label = None

        for net in self.conn.list_nets():
            nettype = virtinst.VirtualNetworkInterface.TYPE_VIRTUAL

            label = self._pretty_network_desc(nettype, net.get_name(), net)
            if not net.is_active():
                label += " (%s)" % _("Inactive")

            if net.get_name() == "default":
                default_label = label

            rows.append(self._build_source_row(
                nettype, net.get_name(), label, True,
                net.is_active(), key=net.get_connkey()))

            # Build a list of vnet bridges, so we know not to list them
            # in the physical interface list
            vnet_bridge = net.get_bridge_device()
            if vnet_bridge:
                vnet_bridges.append(vnet_bridge)

        if not rows:
            label = _("No virtual networks available")
            rows.append(self._build_source_row(
                None, None, label, False, False))

        return rows, vnet_bridges, default_label

    def _find_physical_devices(self, vnet_bridges):
        rows = []
        can_default = False
        default_label = None
        skip_ifaces = ["lo"]

        vnet_taps = []
        for vm in self.conn.list_vms():
            for nic in vm.get_network_devices(refresh_if_nec=False):
                if nic.target_dev and nic.target_dev not in vnet_taps:
                    vnet_taps.append(nic.target_dev)

        netdevs = {}
        for iface in self.conn.list_interfaces():
            netdevs[iface.get_name()] = [
                iface.get_name(), iface.is_bridge(), iface.get_slave_names()]
        for nodedev in self.conn.filter_nodedevs("net"):
            if nodedev.xmlobj.interface not in netdevs:
                netdevs[nodedev.xmlobj.interface] = [nodedev.xmlobj.interface,
                    False, []]

        # For every bridge used by a virtual network, and any slaves of
        # those devices, don't list them.
        for vnet_bridge in vnet_bridges:
            slave_names = netdevs.pop(vnet_bridge, [None, None, []])[2]
            for slave in slave_names:
                netdevs.pop(slave, None)

        for name, is_bridge, slave_names in netdevs.values():
            if ((name in vnet_taps) or
                (name in [v + "-nic" for v in vnet_bridges]) or
                (name in skip_ifaces)):
                # Don't list this, as it is basically duplicating
                # virtual net info
                continue

            sensitive = True
            source_name = name

            label = _("Host device %s") % (name)
            if is_bridge:
                nettype = virtinst.VirtualNetworkInterface.TYPE_BRIDGE
                if slave_names:
                    extra = (_("Host device %s") % slave_names[0])
                    can_default = True
                else:
                    extra = _("Empty bridge")
                label = _("Bridge %s: %s") % (name, extra)

            elif self.conn.check_support(
                    self.conn.SUPPORT_CONN_DIRECT_INTERFACE):
                nettype = virtinst.VirtualNetworkInterface.TYPE_DIRECT
                label += (": %s" % _("macvtap"))

            else:
                nettype = None
                sensitive = False
                source_name = None
                label += (": %s" % _("Not bridged"))

            if can_default and not default_label:
                default_label = label

            rows.append(self._build_source_row(
                nettype, source_name, label, sensitive, True,
                key=name))

        return rows, default_label

    def _populate_network_model(self):
        model = self._network_model

        def _add_manual_bridge_row():
            manual_row = self._build_source_row(
                None, None, _("Specify shared device name"),
                True, False, manual_bridge=True)
            model.append(manual_row)

        if self.conn.is_qemu_session():
            nettype = virtinst.VirtualNetworkInterface.TYPE_USER
            r = self._build_source_row(
                nettype, None, self._pretty_network_desc(nettype), True, True)
            model.append(r)

            _add_manual_bridge_row()
            return

        (vnets, vnet_bridges, default_net) = self._find_virtual_networks()
        (iface_rows, default_bridge) = self._find_physical_devices(
            vnet_bridges)

        # Sorting is:
        # 1) Bridges
        # 2) Virtual networks
        # 3) direct/macvtap
        # 4) Disabled list entries
        # Each category sorted alphabetically
        bridges = [row for row in iface_rows if row[0] == "bridge"]
        direct = [row for row in iface_rows if row[0] == "direct"]
        disabled = [row for row in iface_rows if row[0] is None]

        for rows in [bridges, vnets, direct, disabled]:
            rows.sort(key=lambda r: r[2])
            for row in rows:
                model.append(row)

        # If there is a bridge device, default to that
        # If not, use 'default' network
        # If not present, use first list entry
        # If list empty, use no network devices
        label = default_bridge or default_net

        default = 0
        if not len(model):
            row = self._build_source_row(
                None, None, _("No networking"), True, False)
            model.insert(0, row)
            default = 0
        elif label:
            default = [idx for idx in range(len(model)) if
                       model[idx][2] == label][0]

        _add_manual_bridge_row()
        return default


    ###############
    # Public APIs #
    ###############

    def get_network_row(self):
        if self._selected_network is not None:
            return self._network_model[self._selected_network]

    def get_network_selection(self):
        bridge_entry = self._netbridge_name
        row = self.get_network_row()
        if not row:
            return None, None, None, None

        net_type = row[0]
        net_src = row[1]
        net_check_bridge = row[5]

        if net_check_bridge and bridge_entry is not None:
            net_type = virtinst.VirtualNetworkInterface.TYPE_BRIDGE
            net_src = bridge_entry

        mode = None
        if self._selected_net_source_mode is not None:
            mode = self._selected_net_source_mode

        portgroup = None
        if self._selected_net_portgroup is not None:
            portgroup = self._selected_net_portgroup

        return net_type, net_src, mode, portgroup or None

    def get_vport(self):
        return (self._vport_type, self._vport_managerid, self._vport_typeid,
         self._vport_idver, self._vport_instid)

    def validate_network(self, macaddr, model=None):
        nettype, devname, mode, portgroup = self.get_network_selection()
        if nettype is None:
            return None

        net = None

        # Make sure VirtualNetwork is running
        netobj = None
        if nettype == virtinst.VirtualNetworkInterface.TYPE_VIRTUAL:
            for net in self.conn.list_nets():
                if net.get_name() == devname:
                    netobj = net
                    break

        if netobj and not netobj.is_active():
            # Try to start the network
            try:
                netobj.start()
                logging.info("Started network '%s'", devname)
            except Exception, e:
                return _("Could not start virtual network '%s': %s" % (devname, str(e)))

        # Create network device
        try:
            net = virtinst.VirtualNetworkInterface(self.conn.get_backend())
            net.type = nettype
            net.source = devname
            net.macaddr = macaddr
            net.model = model
            net.source_mode = mode
            net.portgroup = portgroup
            if net.model == "spapr-vlan":
                net.address.set_addrstr("spapr-vio")

            if net.type == "direct":
                (vport_type, vport_managerid, vport_typeid,
                 vport_idver, vport_instid) = self.get_vport()

                net.virtualport.type = vport_type or None
                net.virtualport.managerid = vport_managerid or None
                net.virtualport.typeid = vport_typeid or None
                net.virtualport.typeidversion = vport_idver or None
                net.virtualport.instanceid = vport_instid or None
        except Exception, e:
            return _("Error with network parameters.") + str(e)

        # Make sure there is no mac address collision
        isfatal, errmsg = net.is_conflict_net(net.conn, net.macaddr)
        if isfatal:
            return _("Mac address collision.") + str(errmsg)
        elif errmsg is not None:
            # Mac address collision. but still use this address
            pass

        return net

    def reset_state(self):
        self._network_model = []
        self._selected_network = None
        self._netbridge_name = None
        self._net_source_mode_model = []
        self._selected_net_source_mode = None
        self._net_portgroup_model = []
        self._selected_net_portgroup = None
        self._vport_type = None
        self._vport_managerid = None
        self._vport_typeid = None
        self._vport_idver = None
        self._vport_instid = None

        self._repopulate_network_list()

        net_err = None
        if (not self.conn.is_nodedev_capable() or
            not self.conn.is_interface_capable()):
            net_err = _("Libvirt version does not support "
                        "physical interface listing.")
        if bool(net_err):
            self._add_warn(net_err)

    def set_dev(self, net):
        self.reset_state()

        nettype = net.type
        source = net.source
        source_mode = net.source_mode
        is_direct = (net.type == "direct")

        # uiutil.set_list_selection(self.widget("net-source-mode"), source_mode)
        self._net_source_mode_model = source_mode

        # Virtualport config
        # self.widget("vport-expander").set_visible(is_direct)

        vport = net.virtualport
        self._vport_type = vport.type or ""
        self._vport_managerid = str(vport.managerid or "")
        self._vport_typeid = str(vport.typeid or "")
        self._vport_idver = str(vport.typeidversion or "")
        self._vport_instid = vport.instanceid or ""

        # Find the matching row in the net list
        combo = self._get_network_model()
        rowiter = None
        for row in combo:
            if row[0] == nettype and row[1] == source:
                rowiter = row.iter
                break
        if not rowiter:
            if nettype == "bridge":
                rowiter = combo[-1].iter
                self._netbridge_name = source
        if not rowiter:
            desc = self._pretty_network_desc(nettype, source)
            combo.insert(0,
                self._build_source_row(nettype, source, desc, True, True))
            rowiter = combo[0].iter

        self._selected_network = rowiter
        # combo.emit("changed")

        if net.portgroup:
            self._selected_net_portgroup = net.portgroup

    #############
    # Listeners #
    #############

    def _emit_changed(self, *args, **kwargs):
        ignore1 = args
        ignore2 = kwargs
        self.emit("changed")

    def _emit_vport_changed(self, *args, **kwargs):
        ignore1 = args
        ignore2 = kwargs
        self.emit("changed-vport")

    def _repopulate_network_list(self, *args, **kwargs):
        ignore1 = args
        ignore2 = kwargs

        # netlist = self._get_network_model()
        # current_label = uiutil.get_list_selection(netlist, column=2)

        try:
            # netlist.set_model(None)
            default_idx = self._populate_network_model()
        finally:
            pass
            # netlist.set_model(model)

        # for row in model:
        #     if current_label and row[2] == current_label:
        #         netlist.set_active_iter(row.iter)
        #         return

        if default_idx is None:
            default_idx = 0
        self._selected_network = default_idx
        # netlist.set_active(default_idx)


    def _populate_portgroups(self, portgroups):
        model = self._get_net_portgroup_model()
        model = []

        default = None
        for p in portgroups:
            model.append([p.name, p.name])
            if p.default:
                default = p.name
        
        self._selected_net_portgroup = default

    def _on_net_source_changed(self, src):
        ignore = src
        self._emit_changed()
        row = self.get_network_row()
        if not row:
            return

        is_direct = (row[0] == virtinst.VirtualNetworkInterface.TYPE_DIRECT)
        # self.widget("vport-expander").set_visible(is_direct)
        # uiutil.set_grid_row_visible(self.widget("net-source-mode"), is_direct)
        # uiutil.set_grid_row_visible(
        #     self.widget("net-macvtap-warn-box"), is_direct)
        # if is_direct and self.widget("net-source-mode").get_active() == -1:
        #     self.widget("net-source-mode").set_active(0)

        show_bridge = row[5]
        # uiutil.set_grid_row_visible(
        #     self.widget("net-bridge-name"), show_bridge)

        portgroups = []
        connkey = row[6]
        if connkey and row[0] == virtinst.VirtualNetworkInterface.TYPE_VIRTUAL:
            portgroups = self.conn.get_net(connkey).get_xmlobj().portgroups

        # uiutil.set_grid_row_visible(
        #     self.widget("net-portgroup"), bool(portgroups))
        self._populate_portgroups(portgroups)
