# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

"""
this module provide simple json output for VM Hardware devices.
"""
from virtlib import virtinst

__author__ = 'shanchaobj@inspur.com'

(HW_LIST_COL_LABEL,
 HW_LIST_COL_TYPE,
 HW_LIST_COL_DEVICE) = range(3)

(HW_LIST_TYPE_GENERAL,
 HW_LIST_TYPE_INSPECTION,
 HW_LIST_TYPE_STATS,
 HW_LIST_TYPE_CPU,
 HW_LIST_TYPE_MEMORY,
 HW_LIST_TYPE_BOOT,
 HW_LIST_TYPE_DISK,
 HW_LIST_TYPE_NIC,
 HW_LIST_TYPE_INPUT,
 HW_LIST_TYPE_GRAPHICS,
 HW_LIST_TYPE_SOUND,
 HW_LIST_TYPE_CHAR,
 HW_LIST_TYPE_HOSTDEV,
 HW_LIST_TYPE_VIDEO,
 HW_LIST_TYPE_WATCHDOG,
 HW_LIST_TYPE_CONTROLLER,
 HW_LIST_TYPE_FILESYSTEM,
 HW_LIST_TYPE_SMARTCARD,
 HW_LIST_TYPE_REDIRDEV,
 HW_LIST_TYPE_TPM,
 HW_LIST_TYPE_RNG,
 HW_LIST_TYPE_PANIC) = range(22)


class VMFmtReader(object):
    """
    VMFmtReader format VM object.
    Provide simple json output for VM Hardware device.
    """
    def __init__(self, vm, conn):
        self.conn = conn
        self.vm = vm
        self._hw_list_model = None
        self._populate_hw_list()

    # API.
    def hv(self):
        hypervisor = {}
        # Basic
        hypervisor["hypervisor"] = self.vm.get_pretty_hv_type()
        hypervisor["arch"] = self.vm.get_arch() or "Unknown"
        hypervisor["emulator"] = self.vm.get_emulator() or "None"
        # Firmware
        domcaps = self.vm.get_domain_capabilities()
        hypervisor["firmware"] = domcaps.label_for_firmware_path(self.vm.get_xmlobj().os.loader)
        # Machine settings
        machtype = self.vm.get_machtype() or "Unknown"
        hypervisor["machtype"] = machtype
        # Chipset
        hypervisor["chipset"] = self._chipset_label_from_machine(machtype)
        return hypervisor

    def cpu(self):
        return {
            "host_cpu_count": self.vm.conn.host_active_processor_count(),
            "cpu_count": self.vm.vcpu_count(),
            "max_cpu_count": self.vm.vcpu_max_count()
        }

    def mem(self):
        return {
            "host_memory": int(round(
                                (self.vm.conn.host_memory_size() / 1024))),
            "mem_memory": int(round((self.vm.get_memory() / 1024.0))),
            "mem_maxmem": int(round((self.vm.maximum_memory() / 1024.0)))
        }

    def stats(self):
        return {}

    def storages(self):
        storageinfo = []
        storagelist = self._get_hw_selection(HW_LIST_TYPE_DISK)
        if not len(storagelist):
            return storageinfo
        for storagepack in storagelist:
            storage = storagepack[HW_LIST_COL_DEVICE]
            stginfo = {}
            path = storage.path
            devtype = storage.device
            ro = storage.read_only
            share = storage.shareable
            bus = storage.bus
            removable = storage.removable
            cache = storage.driver_cache
            io = storage.driver_io
            driver_type = storage.driver_type or ""
            serial = storage.serial
            size = "-"
            if path:
                size = _("Unknown")
                vol = self.conn.get_vol_by_path(path)
                if vol:
                    size = vol.get_pretty_capacity()
            is_cdrom = (devtype == virtinst.VirtualDisk.DEVICE_CDROM)
            is_floppy = (devtype == virtinst.VirtualDisk.DEVICE_FLOPPY)
            is_usb = (bus == "usb")
            can_set_removable = (is_usb and (self.conn.is_qemu() or
                                 self.conn.is_test_conn()))
            if removable is None:
                removable = False
            else:
                can_set_removable = True
            pretty_name = self._label_for_device(storage)
            stginfo["storage_source_path"] = path or "-"
            stginfo["storage_target_type"] = pretty_name
            stginfo["storage_readonly"] = ro
            stginfo["storage_readonly"] = not is_cdrom
            stginfo["storage_shareable"] = share
            stginfo["storage_removable"] = removable
            stginfo["storage_can_set_removable"] = can_set_removable
            stginfo["storage_size"] = size
            stginfo["storage_cache"] = cache
            stginfo["storage_io"] = io
            stginfo["storage_format"] = driver_type
            stginfo["storage_serial"] = serial or ""
            storageinfo.append(stginfo)
        return storageinfo

    def networks(self):
        networkinfo = []
        networklist = self._get_hw_selection(HW_LIST_TYPE_NIC)
        if not len(networklist):
            return networkinfo
        for networkpack in networklist:
            network = networkpack[HW_LIST_COL_DEVICE]
            ninfo = {}
            ninfo["network_model"] = network.model
            ninfo["network_macaddr"] = network.macaddr
            networkinfo.append(ninfo)
        return networkinfo

    def _template_output(self):
        diskinfo = []
        disklist = self._get_hw_selection(HW_LIST_TYPE_DISK)
        if not len(disklist):
            return diskinfo
        for diskpack in disklist:
            disk = diskpack[HW_LIST_COL_DEVICE]
            dinfo = {}
            dinfo["disk_format"] = driver_type
            dinfo["disk_serial"] = serial or ""
            diskinfo.append(dinfo)
        return diskinfo

    # background works & api functions
    def _get_hw_selection(self, field):
        return self._hw_list_model[field]

    def _chipset_label_from_machine(self, machine):
        if machine and "q35" in machine:
            return "Q35"
        return "i440FX"

    def _label_for_device(self, dev):
        devtype = dev.virtual_device_type

        if devtype == "disk":
            busstr = virtinst.VirtualDisk.pretty_disk_bus(dev.bus) or ""

            if dev.device == "floppy":
                devstr = _("Floppy")
                busstr = ""
            elif dev.device == "cdrom":
                devstr = _("CDROM")
            elif dev.device == "disk":
                devstr = _("Disk")
            else:
                devstr = dev.device.capitalize()

            if busstr:
                ret = "%s %s" % (busstr, devstr)
            else:
                ret = devstr

            return "%s %s" % (ret, dev.disk_bus_index)

        if devtype == "interface":
            if dev.macaddr:
                return "NIC %s" % dev.macaddr[-9:]
            else:
                return "NIC"

        if devtype == "input":
            if dev.type == "tablet":
                return _("Tablet")
            elif dev.type == "mouse":
                return _("Mouse")
            elif dev.type == "keyboard":
                return _("Keyboard")
            return _("Input")

        if devtype in ["serial", "parallel", "console"]:
            if devtype == "serial":
                label = _("Serial")
            elif devtype == "parallel":
                label = _("Parallel")
            elif devtype == "console":
                label = _("Console")
            if dev.target_port is not None:
                label += " %s" % (int(dev.target_port) + 1)
            return label

        if devtype == "channel":
            label = _("Channel")
            name = dev.pretty_channel_name(dev.target_name)
            if not name:
                name = dev.pretty_type(dev.type)
            if name:
                label += " %s" % name
            return label

        if devtype == "graphics":
            return _("Display %s") % dev.pretty_type_simple(dev.type)
        if devtype == "redirdev":
            return _("%s Redirector %s") % (dev.bus.upper(), dev.vmmindex + 1)
        if devtype == "hostdev":
            return dev.pretty_name()
        if devtype == "sound":
            return _("Sound: %s") % dev.model
        if devtype == "video":
            return _("Video %s") % dev.pretty_model(dev.model)
        if devtype == "filesystem":
            return _("Filesystem %s") % dev.target[:8]
        if devtype == "controller":
            return _("Controller %s") % dev.pretty_desc()

        devmap = {
            "rng": _("RNG"),
            "tpm": _("TPM"),
            "panic": _("Panic Notifier"),
            "smartcard": _("Smartcard"),
            "watchdog": _("Watchdog"),
        }
        return devmap[devtype]

    def _populate_hw_list(self):
        self._hw_list_model = [[] for i in range(22)]

        def add_hw_list_option(title, list_id):
            self._hw_list_model[list_id].append([title, list_id, title])

        add_hw_list_option(_("Overview"), HW_LIST_TYPE_GENERAL)
        add_hw_list_option(_("OS information"), HW_LIST_TYPE_INSPECTION)
        add_hw_list_option(_("Performance"), HW_LIST_TYPE_STATS)
        add_hw_list_option(_("CPUs"), HW_LIST_TYPE_CPU)
        add_hw_list_option(_("Memory"), HW_LIST_TYPE_MEMORY)
        add_hw_list_option(_("Boot Options"), HW_LIST_TYPE_BOOT)
        self._repopulate_hw_list()

    def _repopulate_hw_list(self):
        def dev_cmp(origdev, newdev):
            if isinstance(origdev, str):
                return False
            if origdev == newdev:
                return True
            if not origdev.get_root_xpath():
                return False
            return origdev.get_root_xpath() == newdev.get_root_xpath()

        def add_hw_list_option(name, list_id, dev):
            self._hw_list_model[list_id].append([name, list_id, dev])

        def update_hwlist(hwtype, newdev):
            label = self._label_for_device(newdev)
            for existDev in self._hw_list_model[hwtype]:
                dev = existDev[HW_LIST_COL_DEVICE]
                if dev_cmp(dev, newdev):
                    # Update existing HW info
                    existDev[HW_LIST_COL_DEVICE] = newdev
                    existDev[HW_LIST_COL_LABEL] = label
                    return
            # Add the new HW info
            add_hw_list_option(label, hwtype, newdev)

        for dev in self.vm.get_disk_devices():
            update_hwlist(HW_LIST_TYPE_DISK, dev)
        for dev in self.vm.get_network_devices():
            update_hwlist(HW_LIST_TYPE_NIC, dev)
        for dev in self.vm.get_input_devices():
            update_hwlist(HW_LIST_TYPE_INPUT, dev)
        for dev in self.vm.get_graphics_devices():
            update_hwlist(HW_LIST_TYPE_GRAPHICS, dev)
        for dev in self.vm.get_sound_devices():
            update_hwlist(HW_LIST_TYPE_SOUND, dev)
        for dev in self.vm.get_char_devices():
            update_hwlist(HW_LIST_TYPE_CHAR, dev)
        for dev in self.vm.get_hostdev_devices():
            update_hwlist(HW_LIST_TYPE_HOSTDEV, dev)
        for dev in self.vm.get_redirdev_devices():
            update_hwlist(HW_LIST_TYPE_REDIRDEV, dev)
        for dev in self.vm.get_video_devices():
            update_hwlist(HW_LIST_TYPE_VIDEO, dev)
        for dev in self.vm.get_watchdog_devices():
            update_hwlist(HW_LIST_TYPE_WATCHDOG, dev)
        for dev in self.vm.get_controller_devices():
            # skip USB2 ICH9 companion controllers
            if dev.model in ["ich9-uhci1", "ich9-uhci2", "ich9-uhci3"]:
                continue
            update_hwlist(HW_LIST_TYPE_CONTROLLER, dev)
        for dev in self.vm.get_filesystem_devices():
            update_hwlist(HW_LIST_TYPE_FILESYSTEM, dev)
        for dev in self.vm.get_smartcard_devices():
            update_hwlist(HW_LIST_TYPE_SMARTCARD, dev)
        for dev in self.vm.get_tpm_devices():
            update_hwlist(HW_LIST_TYPE_TPM, dev)
        for dev in self.vm.get_rng_devices():
            update_hwlist(HW_LIST_TYPE_RNG, dev)
        for dev in self.vm.get_panic_devices():
            update_hwlist(HW_LIST_TYPE_PANIC, dev)
