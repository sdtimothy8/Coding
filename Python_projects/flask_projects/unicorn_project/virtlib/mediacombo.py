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

class vmmMediaCombo(object):
    MEDIA_FLOPPY = "floppy"
    MEDIA_CDROM = "cdrom"

    OPTICAL_FIELDS = 4
    (OPTICAL_DEV_PATH,
    OPTICAL_LABEL,
    OPTICAL_HAS_MEDIA,
    OPTICAL_DEV_KEY) = range(OPTICAL_FIELDS)

    def __init__(self, conn, media_type):
        self.conn = conn
        self.media_type = media_type

        self.media = None
        self._media_model = None
        self._selected_media = -1
        self._populated = False
        self._init()

    def _cleanup(self):
        self.conn = None
        self.media = []
        self._selected_media = -1
        self._populated = False

    ##########################
    # Initialization methods #
    ##########################

    def _init(self):
        # [Device path, pretty label, has_media?, device key]
        fields = []
        fields.insert(self.OPTICAL_DEV_PATH, str)
        fields.insert(self.OPTICAL_LABEL, str)
        fields.insert(self.OPTICAL_HAS_MEDIA, bool)
        fields.insert(self.OPTICAL_DEV_KEY, str)
        self._media_model = fields

        self.media = []

        error = None
        if not self.conn.is_nodedev_capable():
            error = _("Libvirt version does not support media listing.")
        return error


    def _set_mediadev_default(self):
        model = self.media
        if len(model) != 0:
            return

        row = [None] * self.OPTICAL_FIELDS
        row[self.OPTICAL_DEV_PATH] = None
        row[self.OPTICAL_LABEL] = _("No device present")
        row[self.OPTICAL_HAS_MEDIA] = False
        row[self.OPTICAL_DEV_KEY] = None
        model.append(row)

    def _pretty_label(self, nodedev):
        media_label = nodedev.xmlobj.media_label
        if not nodedev.xmlobj.media_available:
            media_label = _("No media detected")
        elif not nodedev.xmlobj.media_label:
            media_label = _("Media Unknown")

        return "%s (%s)" % (media_label, nodedev.xmlobj.block)

    def _mediadev_set_default_selection(self):
        # Set the first active cdrom device as selected, otherwise none
        idx = 0
        model = self.media

        if self._selected_media != -1:
            # already a selection, don't change it
            return

        for row in model:
            if row[self.OPTICAL_HAS_MEDIA] is True:
                self._selected_media = idx
                return
            idx += 1

    def _populate_media(self):
        if self._populated:
            return

        self.media = []
        model = self.media

        for nodedev in self.conn.filter_nodedevs(devtype="storage"):
            if not (nodedev.xmlobj.device_type == "storage" and
                    nodedev.xmlobj.drive_type in ["cdrom", "floppy"]):
                continue
            if nodedev.xmlobj.drive_type != self.media_type:
                continue

            row = [None] * self.OPTICAL_FIELDS
            row[self.OPTICAL_DEV_PATH] = nodedev.xmlobj.block
            row[self.OPTICAL_LABEL] = self._pretty_label(nodedev)
            row[self.OPTICAL_HAS_MEDIA] = nodedev.xmlobj.media_available
            row[self.OPTICAL_DEV_KEY] = nodedev.xmlobj.name
            model.append(row)

        self._set_mediadev_default()
        self._mediadev_set_default_selection()
        self._populated = True


    ##############
    # Public API #
    ##############

    def reset_state(self):
        try:
            self._populate_media()
        except:
            logging.debug("Error populating mediadev combo", exc_info=True)

    def get_path(self):
        return self.media[self.OPTICAL_DEV_PATH]

    def has_media(self):
        if len(self.media)>0 and self._selected_media>-1: 
            return self.media[self.OPTICAL_HAS_MEDIA] or False
        return False
