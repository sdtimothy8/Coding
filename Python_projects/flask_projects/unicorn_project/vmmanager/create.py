# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

"""
this module provide api function to create VM
"""
import logging
import time

from virtlib import virtinst
from virtlib import util
from virtlib.netlist import vmmNetworkList
from virtlib.mediacombo import vmmMediaCombo
from storage import VMStorage
from vnc.VNCToken import VNCToken

__author__ = 'shanchaobj@inspur.com'

DETECT_TIMEOUT = 20

DEFAULT_MEM = 1024

(INSTALL_PAGE_ISO,
 INSTALL_PAGE_URL,
 INSTALL_PAGE_PXE,
 INSTALL_PAGE_IMPORT,
 INSTALL_PAGE_CONTAINER_APP,
 INSTALL_PAGE_CONTAINER_OS) = range(6)

_os_type_model = []
_os_variant_model = []

# os type & version


def _init_os_type_model():
    # Kind of a hack, just show linux + windows by default since
    # that's all 98% of people care about
    supportl = ["generic", "linux", "windows"]
    # Move 'generic' to the front of the list
    types = virtinst.OSDB.list_types()
    types.remove("generic")
    types.insert(0, "generic")
    for typename in types:
        supported = (typename in supportl)
        typelabel = typename.capitalize()
        if typename in ["unix"]:
            typelabel = typename.upper()
        _add_os_row(typename, typelabel, supported)


def _add_os_row(name="", label="", supported=False,
                sep=False, action=False):
    row = {"name": name, "label": label, "sep": sep, "supported": supported}
    _os_type_model.append(row)
    _os_variant_model.append([])


def _init_os_variant_model(idx, _type):
    variants = virtinst.OSDB.list_os(typename=_type)
    supportl = virtinst.OSDB.list_os(typename=_type,
                                     only_supported=True)
    for v in variants:
        supported = v in supportl or v.name == "generic"
        _add_os_child_row(idx, v.name, v.label, supported)


def _add_os_child_row(idx, name="", label="", supported=False,
                      sep=False, action=False):
    row = {"name": name, "label": label, "sep": sep, "supported": supported}
    _os_variant_model[idx].append(row)

_init_os_type_model()
for idx in range(len(_os_type_model)):
    os_type = _os_type_model[idx]
    _init_os_variant_model(idx, os_type["name"])
###########################################################
# Helper functions
###########################################################


def _pretty_arch(_a):
    if _a == "armv7l":
        return "arm"
    return _a


def _pretty_storage(size):
    return "%.1f GiB" % float(size)


def _pretty_memory(mem):
    return "%d MiB" % (mem / 1024.0)


# Tracking devices helpers
def _mark_vmm_device(dev):
    setattr(dev, "vmm_create_wizard_device", True)


def _get_vmm_device(guest, devkey):
    for dev in guest.get_devices(devkey):
        if hasattr(dev, "vmm_create_wizard_device"):
            return dev


def _remove_vmm_device(guest, devkey):
    dev = _get_vmm_device(guest, devkey)
    if dev:
        guest.remove_device(dev)


class VMCreator(object):
    """
    VMCreator wrappers helper class create new VM
    """
    def __init__(self, conn):
        # UI
        self.warn_list = []
        self.error_list = []
        # handling
        self.conn = conn
        self._capsinfo = None
        self._guest = None
        self._failed_guest = None
        # model
        self._xen_type_model = None
        self.install_xen_type = None
        self._arch_model = None
        self.install_arch = None
        self._virt_type_model = None
        self.install_virt_type = None
        self._machine_model = None
        self.install_machine = None
        # OS model
        self.install_method = None
        self.install_os_type = None
        self.install_os_version = None
        self.install_os_type_info = None
        self.install_os_version_info = None
        self.install_iso_path = None
        self.install_vm_name = None
        self.install_vm_cpu = None
        self.install_vm_mem = None
        self.install_vm_storage_size = None
        self.install_port = None
        # Distro detection state variables
        self._detect_os_in_progress = False
        self._os_already_detected_for_media = False
        self._show_all_os_was_selected = False
        self._storage_browser = None
        self._netlist = None
        self._Media = None
        self._addstorage = VMStorage(self.conn)
        self._init_state()

    ######################################################################
    # Initial state handling
    ######################################################################
    def _init_state(self):
        init_res = self._init_conn()
        if init_res is not True:
            print init_res, "#############"

    def _set_caps_state(self):
        """
        Set state that is dependent on when capsinfo changes
        """
        self._populate_machine()
        # self.widget("arch-warning-box").hide()

        # Helper state
        is_local = not self.conn.is_remote()
        is_storage_capable = self.conn.is_storage_capable()
        can_storage = (is_local or is_storage_capable)
        is_pv = (self._capsinfo.os_type == "xen")
        is_container = self.conn.is_container()
        can_remote_url = self.conn.get_backend().support_remote_url_install()

        installable_arch = (self._capsinfo.arch in ["i686", "x86_64",
                                                    "ppc64", "ppc64le",
                                                    "ia64", "s390x"])

        if self._capsinfo.arch == "aarch64":
            try:
                guest = self.conn.caps.build_virtinst_guest(self._capsinfo)
                guest.set_uefi_default()
                installable_arch = True
                logging.debug("UEFI found for aarch64, setting it as default.")
            except Exception, e:
                installable_arch = False
                logging.debug("Error checking for aarch64 UEFI default",
                              exc_info=True)
                msg = _("Failed to setup UEFI for AArch64: %s\n"
                        "Install options are limited.") % e
                self._set_warn(msg)

        # # Install Options
        # method_tree = self.widget("method-tree")
        # method_pxe = self.widget("method-pxe")
        # method_local = self.widget("method-local")
        # method_import = self.widget("method-import")
        # method_container_app = self.widget("method-container-app")

        # method_tree.set_sensitive((is_local or can_remote_url) and
        #                           installable_arch)
        # method_local.set_sensitive(not is_pv and can_storage and
        #                            installable_arch)
        # method_pxe.set_sensitive(not is_pv and installable_arch)
        # method_import.set_sensitive(can_storage)
        # virt_methods = [method_local, method_tree, method_pxe, method_import]

        # pxe_tt = None
        # local_tt = None
        # tree_tt = None
        # import_tt = None

        # if not is_local:
        #     if not can_remote_url:
        #         tree_tt = _("Libvirt version does not "
        #                     "support remote URL installs.")
        #     if not is_storage_capable:
        #         local_tt = _("Connection does not support storage manage.")
        #         import_tt = local_tt

        # if is_pv:
        #     base = _("%s installs not available for paravirt guests.")
        #     pxe_tt = base % "PXE"
        #     local_tt = base % "CDROM/ISO"

        # if not installable_arch:
        #     msg = (_("Architecture '%s' is not installable") %
        #            self._capsinfo.arch)
        #     tree_tt = msg
        #     local_tt = msg
        #     pxe_tt = msg

        # if not any([w.get_active() and w.get_sensitive()
        #             for w in virt_methods]):
        #     for w in virt_methods:
        #         if w.get_sensitive():
        #             w.set_active(True)
        #             break

        # if not (is_container or
        #         [w for w in virt_methods if w.get_sensitive()]):
        #     return self._show_startup_error(
        #             _("No install methods available for this connection."),
        #             hideinstall=False)

        # method_tree.set_tooltip_text(tree_tt or "")
        # method_local.set_tooltip_text(local_tt or "")
        # method_pxe.set_tooltip_text(pxe_tt or "")
        # method_import.set_tooltip_text(import_tt or "")

        # # Container install options
        # method_container_app.set_active(True)
        # self.widget("virt-install-box").set_visible(not is_container)
        # self.widget("container-install-box").set_visible(is_container)

        # show_dtb = ("arm" in self._capsinfo.arch or
        #             "microblaze" in self._capsinfo.arch or
        #             "ppc" in self._capsinfo.arch)
        # self.widget("kernel-box").set_visible(not installable_arch)
        # uiutil.set_grid_row_visible(self.widget("dtb"), show_dtb)

    def _init_conn(self):
        try:
            self._populate_conn_state()
        except Exception, e:
            logging.exception("Error setting create wizard conn state.")
            return str(e)
        return True

    def _populate_xen_type(self):
        self._xen_type_model = []
        model = self._xen_type_model

        default = 0
        guests = []
        if self.conn.is_xen() or self.conn.is_test_conn():
            guests = self.conn.caps.guests[:]

        for guest in guests:
            if not guest.domains:
                continue

            gtype = guest.os_type
            dom = guest.domains[0]
            domtype = dom.hypervisor_type
            label = self.conn.pretty_hv(gtype, domtype)

            # Don't add multiple rows for each arch
            for m in model:
                if m[0] == label:
                    label = None
                    break
            if label is None:
                continue

            # Determine if this is the default given by guest_lookup
            if (gtype == self._capsinfo.os_type and
               domtype == self._capsinfo.hypervisor_type):
                default = len(model)

            model.append([label, gtype])

        show = bool(len(model))
        if show:
            self.install_xen_type = default

    def _populate_arch(self):
        self._arch_model = []
        model = self._arch_model

        default = 0
        archs = []
        for guest in self.conn.caps.guests:
            if guest.os_type == self._capsinfo.os_type:
                archs.append(guest.arch)

        # Combine x86/i686 to avoid confusion
        if (self.conn.caps.host.cpu.arch == "x86_64" and
           "x86_64" in archs and "i686" in archs):
            archs.remove("i686")
        archs.sort()

        prios = ["x86_64", "i686", "aarch64", "armv7l", "ppc64", "ppc64le",
                 "s390x"]
        if self.conn.caps.host.cpu.arch not in prios:
            prios = []
        else:
            for p in prios[:]:
                if p not in archs:
                    prios.remove(p)
                else:
                    archs.remove(p)
        if prios:
            if archs:
                prios += [None]
            archs = prios + archs

        default = 0
        if self._capsinfo.arch in archs:
            default = archs.index(self._capsinfo.arch)

        for arch in archs:
            model.append([_pretty_arch(arch), arch])

        # show = not (len(archs) < 2)
        self.install_arch = default

    def _populate_virt_type(self):
        self._virt_type_model = []
        model = self.install_virt_type

        # Allow choosing between qemu and kvm for archs that traditionally
        # have a decent amount of TCG usage, like armv7l. Also include
        # aarch64 which can be used for arm32 VMs as well
        domains = [d.hypervisor_type for d in self._capsinfo.guest.domains[:]]
        if not self.conn.is_qemu():
            domains = []
        elif self._capsinfo.arch in ["i686", "x86_64", "ppc64", "ppc64le"]:
            domains = []

        default = 0
        if self._capsinfo.hypervisor_type in domains:
            default = domains.index(self._capsinfo.hypervisor_type)

        prios = ["kvm"]
        for domain in prios:
            if domain not in domains:
                continue
            domains.remove(domain)
            domains.insert(0, domain)

        for domain in domains:
            label = self.conn.pretty_hv(self._capsinfo.os_type, domain)
            model.append([label, domain])

        # show = bool(len(model) > 1)
        self.install_virt_type = default

    def _populate_machine(self):
        self._machine_model = []
        model = self._machine_model

        machines = self._capsinfo.machines[:]
        if self._capsinfo.arch in ["i686", "x86_64"]:
            machines = []
        machines.sort()

        defmachine = None
        prios = []
        recommended_machine = self._capsinfo.get_recommended_machine()
        if recommended_machine:
            defmachine = recommended_machine
            prios = [defmachine]

        for p in prios[:]:
            if p not in machines:
                prios.remove(p)
            else:
                machines.remove(p)
        if prios:
            machines = prios + [None] + machines

        default = 0
        if defmachine and defmachine in machines:
            default = machines.index(defmachine)

        for m in machines:
            model.append([m])

        show = (len(machines) > 1)
        if show:
            self.install_machine = default
        else:
            # self.widget("machine").emit("changed")
            pass

    def _populate_conn_state(self):
        # self.conn._init_objects(pollnet=True,
                                        #  pollpool=True, polliface=True,
                                        #  pollnodedev=True)
        self._capsinfo = None
        self.conn.invalidate_caps()
        self._change_caps()
        if not self._capsinfo.guest.has_install_options():
            error = _("No hypervisor options were found for this "
                      "connection.")

            if self.conn.is_qemu():
                error += "\n\n"
                error += _("This usually means that QEMU or KVM is not "
                           "installed on your machine, or the KVM kernel "
                           "modules are not loaded.")
            return error

        # A bit out of order, but populate the xen/virt/arch/machine lists
        # so we can work with a default.
        self._populate_xen_type()
        self._populate_arch()
        self._populate_virt_type()

        # show_arch = (self.widget("xen-type").get_visible() or
        #              self.widget("virt-type").get_visible() or
        #              self.widget("arch").get_visible() or
        #              self.widget("machine").get_visible())
        # uiutil.set_grid_row_visible(self.widget("arch-expander"), show_arch)

        if self.conn.is_xen():
            has_hvm_guests = False
            for g in self.conn.caps.guests:
                if g.os_type == "hvm":
                    has_hvm_guests = True

            if not has_hvm_guests:
                error = _("Host is not advertising support for full "
                          "virtualization. Install options may be limited.")
                self._set_warn(error)

        elif self.conn.is_qemu():
            if not self._capsinfo.guest.is_kvm_available():
                error = _("KVM is not available. This may mean the KVM "
                          "package is not installed, "
                          "or the KVM kernel modules "
                          "are not loaded. Your virtual "
                          "machines may perform poorly.")
                self._set_warn(error)

        # Install local
        if self._Media:
            self._Media.cleanup()
            self._Media = None
        self._Media = vmmMediaCombo(self.conn, vmmMediaCombo.MEDIA_CDROM)

        # self._Media.connect("changed", self._cdrom_changed)
        self._Media.reset_state()

        # Don't select physical CDROM if no valid media is present
        cdrom_option = self._Media.has_media()
        iso_option = not self._Media.has_media()

        enable_phys = not self._stable_defaults()
        cdrom_option = enable_phys
        cdrom_option_tooltip_text = ("" if enable_phys else
                                     _("Physical CDROM passthrough "
                                       "not supported with this hypervisor"))

        # Only allow ISO option for remote VM
        is_local = not self.conn.is_remote()
        if not is_local or not enable_phys:
            iso_option = True

        # self._local_media_toggled(cdrom_option)

        # Memory
        memory = int(self.conn.host_memory_size())
        self._set_config_vm_mem(DEFAULT_MEM)

        # CPU
        phys_cpus = int(self.conn.host_active_processor_count())
        self._set_config_vm_cpu(1)

        # Storage
        self._addstorage.conn = self.conn
        self._addstorage.reset_state()

        # Networking
        if self._netlist:
            self._netlist.cleanup()
            self._netlist = None

        self._netlist = vmmNetworkList(self.conn)
        # self._netlist.connect("changed", self._netdev_changed)
        self._netlist.reset_state()

    ######################################################################
    # Helper functions
    ######################################################################
    def _stable_defaults(self):
        emu = None
        if self._guest:
            emu = self._guest.emulator
        elif self._capsinfo:
            emu = self._capsinfo.emulator

        ret = self.conn.stable_defaults(emu)
        return ret

    # message
    def _set_warn(self, error):
        self.warn_list.append(error)

    def _set_error(self, error):
        self.error_list.append(error)

    def get_warns(self):
        return self.warn_list

    def get_errors(self):
        return self.error_list

    # set user happy value
    def _set_config_vm_name(self, name):
        self.install_vm_name = name

    def _set_config_vm_mem(self, size):
        self.install_vm_mem = size

    def _set_config_vm_cpu(self, count):
        self.install_vm_cpu = count

    def _set_config_vm_storage_size(self, size):
        self._addstorage.set_config_storage_size(size)

    def _set_config_install_method(self, method):
        if method in [INSTALL_PAGE_ISO, INSTALL_PAGE_URL,
                      INSTALL_PAGE_PXE, INSTALL_PAGE_IMPORT,
                      INSTALL_PAGE_CONTAINER_APP,
                      INSTALL_PAGE_CONTAINER_OS]:
            self.install_method = method
            # default use local iso
            self.install_method = INSTALL_PAGE_ISO

    def _set_config_media_path(self, path):
        self.install_iso_path = path
        # if self.install_method in [INSTALL_PAGE_ISO, INSTALL_PAGE_URL]:
        #     cdrom = self._Media.has_media()
        #     self._local_media_toggled(cdrom)

    def _set_config_vm_port(self, port):
        self.install_port = port

    def _set_config_os_distro(self, types, name):
        self.install_os_type = types
        self.install_os_version = name

    def _set_distro(self, variant):
        distro_type = None
        distro_var = None
        if variant:
            osclass = virtinst.OSDB.lookup_os(variant)
            distro_type = osclass.get_typename()
            distro_var = osclass.name
        self.install_os_type = distro_type
        self.install_os_version = distro_var
        for idx in range(len(_os_type_model)):
            type_info = _os_type_model[idx]
            if type_info["name"] == distro_type:
                self.install_os_type_info = type_info["label"]
                childlist = _os_variant_model[idx]
                for version_info in childlist:
                    if version_info["name"] == distro_var:
                        self.install_os_version_info = version_info["label"]

    # get user happy value

    def _get_config_vm_name(self):
        return self.install_vm_name

    def _get_config_vm_mem(self):
        return self.install_vm_mem

    def _get_config_vm_cpu(self):
        return self.install_vm_cpu

    def _get_config_vm_storage_size(self):
        return self._addstorage.get_config_storage_size()

    def _get_config_install_method(self):
        # default use local iso
        return self.install_method

    def _get_config_os_info(self):
        return (self.install_os_type and str(self.install_os_type),
                self.install_os_version and str(self.install_os_version),
                str(self.install_os_type_info or ""),
                str(self.install_os_version_info))

    def _get_config_media_path(self):
        return self.install_iso_path

    def _get_config_vm_port(self):
        return self.install_port

    def _get_config_os_distro(self):
        return self.install_distro

    def _get_config_detectable_media(self):
        instpage = self._get_config_install_method()
        media = ""

        if instpage == INSTALL_PAGE_ISO:
            media = self._get_config_media_path()
        # # default use local iso
        # elif instpage == INSTALL_PAGE_URL:
        #     media = self.widget("install-url-entry").get_text()
        # elif instpage == INSTALL_PAGE_IMPORT:
        #     media = self.widget("install-import-entry").get_text()

        return media

    def _is_default_storage(self):
        return (self._addstorage.is_default_storage() and
                not self._should_skip_disk_page())

    def _should_skip_disk_page(self):
        return self._get_config_install_method() in [
            INSTALL_PAGE_IMPORT,
            INSTALL_PAGE_CONTAINER_APP,
            INSTALL_PAGE_CONTAINER_OS]
    # media functions, os type & version
    # def _detectable_media_changed(self):
    #     self._os_already_detected_for_media = False
    #     self._do_start_detect_os(self._get_config_os_distro())

    # def _iso_changed(self):
    #     self._detectable_media_changed()

    # def _cdrom_changed(self):
    #     self._detectable_media_changed()

    # def _local_media_toggled(self, option):
    #     if option:
    #         self._cdrom_changed()
    #     else:
    #         self._iso_changed()

    # def _do_start_detect_os(self, distro):
    #     # self._detect_os_in_progress = True
    #     # logging.debug("Starting OS detection for media=%s", media)
    #     # distro = self._detect_os(media)
    #     if distro is None:
    #         return False
    #     self._os_already_detected_for_media = True
    #     self._detect_os_in_progress = False
    #     self._set_distro(distro)
    #     return True

    # def _detect_os(self, path):
    #     try:
    #         installer = virtinst.DistroInstaller(self.conn.get_backend())
    #         installer.location = path
    #         distro = installer.detect_distro(self._guest)
    #         print distro
    #     except:
    #         logging.exception("Error detecting distro.")
    #         return None
    #     return distro

    # validation functions
    def _change_caps(self, gtype=None, arch=None, domtype=None):
        """
        Change the cached capsinfo for the passed values, and trigger
        all needed UI refreshing
        """
        if gtype is None:
            # If none specified, prefer HVM so install options aren't limited
            # with a default PV choice.
            for g in self.conn.caps.guests:
                if g.os_type == "hvm":
                    gtype = "hvm"
                    break

        capsinfo = self.conn.caps.guest_lookup(os_type=gtype,
                                               arch=arch,
                                               typ=domtype)

        if self._capsinfo:
            if (self._capsinfo.guest == capsinfo.guest and
               self._capsinfo.domain == capsinfo.domain):
                return

        self._capsinfo = capsinfo
        logging.debug("Guest type set to os_type=%s, arch=%s, dom_type=%s",
                      self._capsinfo.os_type,
                      self._capsinfo.arch,
                      self._capsinfo.hypervisor_type)
        self._set_caps_state()

    def _build_guest(self, variant):
        guest = self.conn.caps.build_virtinst_guest(self._capsinfo)
        # UUID
        try:
            guest.uuid = util.randomUUID(guest.conn)
        except Exception, e:
            # self.err.show_err(_("Error setting UUID: %s") % str(e))
            return None
        # OS distro/variant validation
        try:
            if variant:
                guest.os_variant = variant
        except ValueError, e:
            # self.err.val_err(_("Error setting OS information."), str(e))
            return None

        if guest.os.is_arm64():
            try:
                guest.set_uefi_default()
            except:
                # If this errors we will have already informed the user
                # on page 1.
                return None

        # Set up default devices
        try:
            guest.default_graphics_type = "vnc"
            guest.skip_default_sound = False
            guest.skip_default_usbredir = False
            guest.x86_cpu_default = "host-model-only"
            guest.add_default_devices()
        except Exception, e:
            return None
        return guest

    def _generate_default_name(self, distro, variant):
        force_num = False
        if self._guest.os.is_container():
            basename = "container"
            force_num = True
        elif not distro:
            basename = "vm"
            force_num = True
        elif not variant:
            basename = distro
        else:
            basename = variant

        if self._guest.os.arch != self.conn.caps.host.cpu.arch:
            basename += "-%s" % _pretty_arch(self._guest.os.arch)
            force_num = False
        return util.generate_name(basename,
                                  self.conn.get_backend().lookupByName,
                                  start_num=force_num and 1 or 2,
                                  force_num=force_num,
                                  sep=not force_num and "-" or "",
                                  collidelist=[vm.get_name() for vm in
                                               self.conn.list_vms()])

    def _validate_install_source(self):
        instmethod = self._get_config_install_method()
        installer = None
        location = None
        extra = None
        cdrom = False
        is_import = False
        init = None
        fs = None
        distro, variant, ignore1, ignore2 = self._get_config_os_info()
        if not distro:
            return _("Please specify a valid OS variant.")

        if instmethod == INSTALL_PAGE_ISO:
            instclass = virtinst.DistroInstaller
            media = self._get_config_media_path()
            if not media:
                return _("An install media selection is required.")
            location = media
            cdrom = True

        elif instmethod == INSTALL_PAGE_URL:
            instclass = virtinst.DistroInstaller
            media, extra = self._get_config_media_path()
            if not media:
                return self.err.val_err(_("An install tree is required."))
            location = media

        elif instmethod == INSTALL_PAGE_PXE:
            instclass = virtinst.PXEInstaller

        elif instmethod == INSTALL_PAGE_IMPORT:
            instclass = virtinst.ImportInstaller
            is_import = True

            import_path = self._get_config_media_path()
            if not import_path:
                return _("A storage path to import is required.")

            if not virtinst.VirtualDisk.path_definitely_exists(
                                                self.conn.get_backend(),
                                                import_path):
                return _("The import path must point to an existing storage.")
        # TODO:INSTALL_PAGE_CONTAINER_APP & INSTALL_PAGE_CONTAINER_OS
        # elif instmethod == INSTALL_PAGE_CONTAINER_APP:
        #     instclass = virtinst.ContainerInstaller
        #     init = self.widget("install-app-entry").get_text()
        #     if not init:
        #         return _("An application path is required.")

        # elif instmethod == INSTALL_PAGE_CONTAINER_OS:
        #     instclass = virtinst.ContainerInstaller
        #     fs = self.widget("install-oscontainer-fs").get_text()
        #     if not fs:
        #         return _("An OS directory path is required.")

        # Build the installer and Guest instance
        try:
            # Overwrite the guest
            installer = instclass(self.conn.get_backend())
            self._guest = self._build_guest(variant or distro)
            if not self._guest:
                return False
            self._guest.installer = installer
        except Exception, e:
            return _("Error setting installer parameters.") + str(e)

        # Validate media location
        try:
            if location is not None:
                self._guest.installer.location = location
            if cdrom:
                self._guest.installer.cdrom = True
            if extra:
                self._guest.installer.extraargs = [extra]
            # TODO:INSTALL_PAGE_CONTAINER_APP & INSTALL_PAGE_CONTAINER_OS
            # if init:
            #     self._guest.os.init = init
            # if fs:
            #     fsdev = virtinst.VirtualFilesystem(self._guest.conn)
            #     fsdev.target = "/"
            #     fsdev.source = fs
            #     self._guest.add_device(fsdev)
        except Exception, e:
            return _("Error setting install media location.") + str(e)

        # TODO:INSTALL_PAGE_IMPORT
        # Setting kernel
        # if instmethod == INSTALL_PAGE_IMPORT:
        #     kernel = self.widget("kernel").get_text() or None
        #     kargs = self.widget("kernel-args").get_text() or None
        #     initrd = self.widget("initrd").get_text() or None
        #     dtb = self.widget("dtb").get_text() or None

        #     if not self.widget("dtb").get_visible():
        #         dtb = None
        #     if not self.widget("kernel").get_visible():
        #         kernel = None
        #         initrd = None
        #         kargs = None

        #     self._guest.os.kernel = kernel
        #     self._guest.os.initrd = initrd
        #     self._guest.os.dtb = dtb
        #     self._guest.os.kernel_args = kargs

        #     require_kernel = ("arm" in self._capsinfo.arch)
        #     if require_kernel and not kernel:
        #         return self.err.val_err(
        #             _("A kernel is required for %s guests.") %
        #             self._capsinfo.arch)

        try:
            name = self._generate_default_name(distro, variant)
            self._guest.name = name
        except Exception, e:
            return _("Error setting default name.") + str(e)

        # Kind of wonky, run storage validation now, which will assign
        # the import path. Import installer skips the storage page.
        # TODO:
        # if is_import:
        #     if not self._validate_storage_page():
        #         return False
        if self._guest.installer.scratchdir_required():
            path = util.make_scratchdir(self._guest.conn, self._guest.type)
        elif instmethod == INSTALL_PAGE_ISO:
            path = self._guest.installer.location
        else:
            path = None
        if path:
            self._addstorage.check_path_search(
                self, self.conn, path)

        # res = None
        # osobj = virtinst.OSDB.lookup_os(variant)
        # if osobj:
        #     res = osobj.get_recommended_resources(self._guest)
        #     logging.debug("Recommended resources for variant=%s: %s",
        #         variant, res)

        # # Change the default values suggested to the user.
        # ram_size = DEFAULT_MEM
        # if res and res.get("ram") > 0:
        #     ram_size = res["ram"] / (1024 ** 2)
        # self._set_config_vm_mem(ram_size)

        # n_cpus = 1
        # if res and res.get("n-cpus") > 0:
        #     n_cpus = res["n-cpus"]
        # self._set_config_vm_cpu(n_cpus)

        # if res and res.get("storage"):
        #     storage_size = int(res["storage"]) / (1024 ** 3)
        #     self._set_config_vm_storage_size(storage_size)

        return True

    def _validate_install_vdevice(self):
        cpus = self._get_config_vm_cpu()
        mem = self._get_config_vm_mem()
        # VCPUS
        try:
            self._guest.vcpus = int(cpus)
        except Exception, e:
            return _("Error setting CPUs.") + str(e)
        # Memory
        try:
            self._guest.memory = int(mem) * 1024
            self._guest.maxmemory = int(mem) * 1024
        except Exception, e:
            return _("Error setting guest memory.") + str(e)

        return True

    def _get_storage_path(self, vmname, do_log):
        failed_disk = None
        if self._failed_guest:
            failed_disk = _get_vmm_device(self._failed_guest, "disk")

        path = None
        path_already_created = False

        if self._get_config_install_method() == INSTALL_PAGE_IMPORT:
            path = self._get_config_media_path()

        elif self._is_default_storage():
            if failed_disk:
                # Don't generate a new path if the install failed
                path = failed_disk.path
                path_already_created = failed_disk.storage_was_created
                if do_log:
                    logging.debug("Reusing failed disk path=%s "
                                  "already_created=%s", path,
                                  path_already_created)
            else:
                path = self._addstorage.get_default_path(vmname)
                if do_log:
                    logging.debug("Default storage path is: %s", path)

        return path, path_already_created

    def _validate_install_storage(self):
        path, path_already_created = self._get_storage_path(
            self._guest.name, do_log=True)
        disk = None
        storage_enabled = True
        try:
            if storage_enabled:
                disk = self._addstorage.validate_storage(self._guest.name,
                                                         path=path)

        except Exception, e:
            return _("Storage parameter error.") + str(e)

        if disk is False:
            return False

        if self._get_config_install_method() == INSTALL_PAGE_ISO:
            # CD/ISO install and no disks implies LiveCD
            self._guest.installer.livecd = not storage_enabled

        if disk and self._addstorage.validate_disk_object(disk) is False:
            return False

        _remove_vmm_device(self._guest, "disk")

        if not storage_enabled:
            return True

        disk.storage_was_created = path_already_created
        _mark_vmm_device(disk)
        self._guest.add_device(disk)

        return True

    def _validate_install_dev(self):
        # HV + Arch selection
        name = self._get_config_vm_name()
        if name != self._guest.name:
            try:
                self._guest.name = name
            except Exception, e:
                return _("Invalid guest name") + str(e)
            if self._is_default_storage():
                logging.debug("User changed VM name and using default "
                              "storage, re-validating with new default "
                              "storage path.")
                # User changed the name and we are using default storage
                # which depends on the VM name. Revalidate things
                if self._validate_install_storage() is not True:
                    return False

        nettype = self._netlist.get_network_selection()[0]
        if nettype is None:
            # No network device available
            instmethod = self._get_config_install_method()
            methname = None
            if instmethod == INSTALL_PAGE_PXE:
                methname = "PXE"
            elif instmethod == INSTALL_PAGE_URL:
                methname = "URL"

            if methname:
                return _("Network device required for %s install.") % methname

        macaddr = virtinst.VirtualNetworkInterface.generate_mac(
            self.conn.get_backend())
        nic = self._netlist.validate_network(macaddr)
        if nic is False:
            return False

        _remove_vmm_device(self._guest, "interface")
        if nic:
            _mark_vmm_device(nic)
            self._guest.add_device(nic)

        # set vnc
        self._guest.set_vnc_port(self._get_config_vm_port())

        return True
    # do install

    def _start_install(self, guest, return_xml=False):
        if return_xml:
            return guest.start_install(return_xml=True)
        self._failed_guest = None
        logging.debug("Starting background install process")
        guest.start_install()
        logging.debug("Install completed")
        # Wait for VM to show up
        # self.conn._init_objects(pollvm=True)
        count = 0
        foundvm = None
        # while count < 100:
        #     for vm in self.conn.list_vms():
        #         if vm.get_uuid() == guest.uuid:
        #             foundvm = vm
        #     if foundvm:
        #         break
        #     count += 1
        #     time.sleep(.1)
        self.conn._populate_objects(pollvm=True)
        for vm in self.conn.list_vms():
            if vm.get_uuid() == guest.uuid:
                foundvm = vm
                break
        if not foundvm:
            return False, _("VM '%s' didn't show up after expected time." %
                            guest.name)
        vm = foundvm
        if vm.is_shutoff():
            # Domain is already shutdown, but no error was raised.
            # Probably means guest had no 'install' phase, as in
            # for live cds. Try to restart the domain.
            vm.startup()
        elif guest.installer.has_install_phase():
            # Register a status listener, which will restart the
            # guest after the install has finished
            # def cb():
            #     vm.connect_opt_out("state-changed",
            #                        self._check_install_status)
            #     return False
            # self.idle_add(cb)
            pass

        return True, vm

    def _check_install_status(self, vm):
        """
        Watch the domain that we are installing, waiting for the state
        to change, so we can restart it as needed
        """
        if vm.is_crashed():
            logging.debug("VM crashed, cancelling install plans.")
            return True

        if not vm.is_shutoff():
            return

        if vm.get_install_abort():
            logging.debug("User manually shutdown VM, not restarting "
                          "guest after install.")
            return True

        try:
            logging.debug("Install should be completed, starting VM.")
            vm.startup()
        except Exception, e:
            self.err.show_err(_("Error continue install: %s") % str(e))

        return True

    ######################################################################
    # API FUNCITON
    ######################################################################
    def set_config(self, name, os_type, os_name, path,
                   method=INSTALL_PAGE_ISO, cpus=1,
                   mem=1024, size=10, port=15900):
        self._set_config_vm_name(name)
        self._set_config_install_method(INSTALL_PAGE_ISO)
        self._set_config_os_distro(os_type, os_name)
        self._set_config_media_path(path)
        message = self._validate_install_source()
        if message is not True:
            return (False, message)
        self._set_config_vm_cpu(cpus)
        self._set_config_vm_mem(mem)
        message = self._validate_install_vdevice()
        if message is not True:
            return (False, message)
        self._set_config_vm_storage_size(size)
        message = self._validate_install_storage()
        if message is not True:
            return (False, message)
        self._set_config_vm_port(port)
        message = self._validate_install_dev()
        if message is not True:
            return (False, message)
        return (True, True)

    def start_install(self):
        logging.debug("Starting create vmcreator prepare sequence")
        return self._start_install(self._guest)

    def start_install_xml(self):
        return self._start_install(self._guest, return_xml=True)

    @staticmethod
    def host_space(conn):
        return VMStorage.host_space(conn)

    @staticmethod
    def default_dir(conn):
        return VMStorage.default_dir(conn)

    @staticmethod
    def detect_os(path):
        typeinfo = None
        versioninfo = None
        distro = None
        try:
            distro = virtinst.OSDB.lookup_os_by_media(path)
        except:
            try:
                distro = virtinst.OSDB.lookup_os_by_media(path)
            except:
                try:
                    distro = virtinst.OSDB.lookup_os_by_media(path)
                except:
                    pass
        if distro:
            osclass = virtinst.OSDB.lookup_os(distro)
            distro_type = osclass.get_typename()
            distro_var = osclass.name
            for idx in range(len(_os_type_model)):
                type_info = _os_type_model[idx]
                if type_info[OS_COL_ID] == distro_type:
                    typeinfo = type_info[OS_COL_LABEL]
                    childlist = _os_variant_model[idx]
                    for version_info in childlist:
                        if version_info[OS_COL_ID] == distro_var:
                            versioninfo = version_info[OS_COL_LABEL]
        return typeinfo, versioninfo
