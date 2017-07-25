#
# Copyright (C) 2016 Inspur Group.
# Author ShanChao(Vagary) <shanchaobj@inspur.com>
#
# This package is all free; you can redistribute it and/or modify
# it under the terms of License.
#

# Copyright (C) 2013, 2014 Red Hat, Inc.
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



# pylint: disable=wrong-import-position

import __builtin__
__builtin__.__dict__['_'] = unicode

from . import util
from . import support
from .uri import URI
from .osdict import OSDB

from .osxml import OSXML
from .domainfeatures import DomainFeatures
from .domainnumatune import DomainNumatune
from .domainblkiotune import DomainBlkiotune
from .domainmemorytune import DomainMemorytune
from .domainmemorybacking import DomainMemorybacking
from .domainresource import DomainResource
from .clock import Clock
from .cpu import CPU, CPUFeature
from .seclabel import Seclabel
from .pm import PM
from .idmap import IdMap

from .capabilities import Capabilities
from .domcapabilities import DomainCapabilities
from .interface import Interface, InterfaceProtocol
from .network import Network
from .nodedev import NodeDevice
from .storage import StoragePool, StorageVolume

from .device import VirtualDevice
from .deviceinterface import VirtualNetworkInterface
from .devicegraphics import VirtualGraphics
from .deviceaudio import VirtualAudio
from .deviceinput import VirtualInputDevice
from .devicedisk import VirtualDisk
from .devicehostdev import VirtualHostDevice
from .devicechar import (VirtualChannelDevice,
                                 VirtualConsoleDevice,
                                 VirtualParallelDevice,
                                 VirtualSerialDevice)
from .devicevideo import VirtualVideoDevice
from .devicecontroller import VirtualController
from .devicewatchdog import VirtualWatchdog
from .devicefilesystem import VirtualFilesystem
from .devicesmartcard import VirtualSmartCardDevice
from .deviceredirdev import VirtualRedirDevice
from .devicememballoon import VirtualMemballoon
from .devicetpm import VirtualTPMDevice
from .devicerng import VirtualRNGDevice
from .devicepanic import VirtualPanicDevice

from .installer import (ContainerInstaller, ImportInstaller,
                                PXEInstaller, Installer)

from .distroinstaller import DistroInstaller

from .guest import Guest
from .cloner import Cloner
from .snapshot import DomainSnapshot

from .connection import VirtualConnection
