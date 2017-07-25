# -*- coding: utf-8 -*-

"""Common objects shared by all unicon modules."""

import os
import sys

# Global information
appname = 'system_monitor'
# version = __import__('system_monitor').__version__
version = "1.0"
# psutil_version = __import__('system_monitor').__psutil_version
try:
    from psutil import __version__ as psutil_version
except ImportError:
    psutil_version = "0.0"

# PY3?
is_py3 = sys.version_info >= (3, 3)

# Operating system flag
# Note: Somes libs depends of OS
is_bsd = sys.platform.find('bsd') != -1
is_linux = sys.platform.startswith('linux')
is_mac = sys.platform.startswith('darwin')
is_windows = sys.platform.startswith('win')

# Path definitions
work_path = os.path.realpath(os.path.dirname(__file__))
appname_path = os.path.split(sys.argv[0])[0]
sys_prefix = os.path.realpath(os.path.dirname(appname_path))

# Set the plugins path
plugins_path = os.path.realpath(os.path.join(work_path, '..', 'plugins'))

# Set the export module path
exports_path = os.path.realpath(os.path.join(work_path, '..', 'exports'))

sys_path = sys.path[:]
sys.path.insert(1, plugins_path)
sys.path.insert(1, exports_path)
