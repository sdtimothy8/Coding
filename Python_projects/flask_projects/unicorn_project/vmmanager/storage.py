# coding=utf8
#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

import logging
import os
import statvfs
from virtlib import virtinst


class VMStorage(object):

    def __init__(self, conn):
        self.conn = conn
        self.host_space = None
        self.storage_path = None
        self.storage_size = None

    def _cleanup(self):
        self.conn = None

    ##########################
    # Initialization methods #
    ##########################

    def _get_default_dir(self):
        return virtinst.StoragePool.get_default_dir(self.conn.get_backend())

    def _get_ideal_path_info(self, name):
        path = self._get_default_dir()
        fmt = self.conn.get_default_storage_format()
        suffix = virtinst.StorageVolume.get_file_extension_for_format(fmt)
        return (path, name, suffix or ".img")

    def _get_ideal_path(self, name):
        target, name, suffix = self._get_ideal_path_info(name)
        return os.path.join(target, name) + suffix

    def _host_disk_space(self):
        pool = self.conn.get_default_pool()
        path = self._get_default_dir()

        avail = 0
        if pool and pool.is_active():
            # Rate limit this, since it can be spammed at dialog startup time
            if pool.secs_since_last_refresh() > 10:
                pool.refresh()
            avail = int(pool.get_available())

        elif not self.conn.is_remote() and os.path.exists(path):
            vfs = os.statvfs(os.path.dirname(path))
            avail = vfs[statvfs.F_FRSIZE] * vfs[statvfs.F_BAVAIL]

        return float(avail / 1024.0 / 1024.0 / 1024.0)

    @staticmethod
    def default_dir(conn):
        return virtinst.StoragePool.get_default_dir(conn.get_backend())

    @staticmethod
    def host_space(conn):
        pool = conn.get_default_pool()
        path = virtinst.StoragePool.get_default_dir(conn.get_backend())
        avail = 0
        if pool and pool.is_active():
            # Rate limit this, since it can be spammed at dialog startup time
            if pool.secs_since_last_refresh() > 10:
                pool.refresh()
            avail = int(pool.get_available())

        elif not conn.is_remote() and os.path.exists(path):
            vfs = os.statvfs(os.path.dirname(path))
            avail = vfs[statvfs.F_FRSIZE] * vfs[statvfs.F_BAVAIL]

        return float(avail / 1024.0 / 1024.0 / 1024.0)

    def _update_host_space(self):
        try:
            max_storage = self._host_disk_space()
        except:
            logging.exception("Error determining host disk space")
            return

        def pretty_storage(size):
            return "%.1f GiB" % float(size)
        self.host_space = pretty_storage(max_storage)
        return max_storage

    def _check_default_pool_active(self):
        default_pool = self.conn.get_default_pool()
        if default_pool and not default_pool.is_active():
            # Default pool is not active.Storage pool is not active.
            # Try to start the pool now
            try:
                default_pool.start()
                logging.info("Started pool '%s'", default_pool.get_name())
            except Exception, e:
                return _("Could not start storage_pool '%s': %s" % (
                         default_pool.get_name(), str(e)))
        return True

    ##############
    # Public API #
    ##############
    def set_config_storage_path(self, path):
        self.storage_path = path

    def get_config_storage_path(self):
        return self.storage_path

    def set_config_storage_size(self, size):
        self.storage_size = size

    def get_config_storage_size(self):
        return self.storage_size

    @staticmethod
    def check_path_search(src, conn, path):
        skip_paths = []
        user, broken_paths = virtinst.VirtualDisk.check_path_search(
            conn.get_backend(), path)

        for p in broken_paths[:]:
            if p in skip_paths:
                broken_paths.remove(p)

        if not broken_paths:
            return True

        logging.debug("No search access for dirs: %s", broken_paths)
        # The emulator may not have search permissions for the path
        # correct this now
        # src.config.add_perms_fix_ignore(broken_paths)

        logging.debug("Attempting to correct permission issues.")
        errors = virtinst.VirtualDisk.fix_path_search_for_user(
            conn.get_backend(), path, user)
        if not errors:
            return True

        return False

    def reset_state(self):
        self._update_host_space()

    def is_default_storage(self):
        return self.storage_path is None or (os.path.dirname(self.storage_path) == self._get_default_dir())

    def get_default_path(self, name, collidelist=None):
        collidelist = collidelist or []
        pool = self.conn.get_default_pool()

        default_dir = self._get_default_dir()

        def path_exists(p):
            return os.path.exists(p) or p in collidelist

        if not pool:
            # Use old generating method
            origf = os.path.join(default_dir, name + ".img")
            f = origf

            n = 1
            while path_exists(f) and n < 100:
                f = os.path.join(default_dir, name +
                                 "-" + str(n) + ".img")
                n += 1

            if path_exists(f):
                f = origf

            path = f
        else:
            target, ignore, suffix = self._get_ideal_path_info(name)

            # Sanitize collidelist to work with the collision checker
            newcollidelist = []
            for c in collidelist:
                if c and os.path.dirname(c) == pool.get_target_path():
                    newcollidelist.append(os.path.basename(c))

            path = virtinst.StorageVolume.find_free_name(
                pool.get_backend(), name,
                suffix=suffix, collidelist=newcollidelist)

            path = os.path.join(target, path)

        return path

    def validate_storage(self, vmname, path=None,
                         device="disk", collidelist=None):
        if path is None:
            path = self.get_config_storage_path()
        if path is None:
            path = self.get_default_path(vmname, collidelist or [])
            ret = self._check_default_pool_active()
            if ret is not True:
                return False

        if not path and device in ["disk", "lun"]:
            return _("A storage path must be specified.")

        disk = virtinst.VirtualDisk(self.conn.get_backend())
        disk.path = path or None
        disk.device = device

        if disk.wants_storage_creation():
            pool = disk.get_parent_pool()
            size = self.get_config_storage_size()
            sparse = False
            vol_install = virtinst.VirtualDisk.build_vol_install(
                disk.conn, os.path.basename(disk.path), pool,
                size, sparse)
            disk.set_vol_install(vol_install)
            fmt = self.conn.get_default_storage_format()
            if fmt in disk.get_vol_install().list_formats():
                logging.debug("Using default prefs format=%s for path=%s",
                              fmt, disk.path)
                disk.get_vol_install().format = fmt
            else:
                logging.debug("path=%s can not use default prefs format=%s, "
                              "not setting it", disk.path, fmt)

        disk.validate()
        return disk

    def validate_disk_object(self, disk):
        isfatal, errmsg = disk.is_size_conflict()
        if not isfatal and errmsg:
            return _("Not Enough Free Space") + str(errmsg)

        # Disk collision
        names = disk.is_conflict_disk()
        if names:
            return _('Disk "%s" is already in use by other guests %s' %
                     (disk.path, names))

        return self.check_path_search(self, self.conn, disk.path)
