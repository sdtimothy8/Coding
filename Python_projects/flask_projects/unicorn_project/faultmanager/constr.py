# coding=utf-8
__author__ = 'zhuysh@inspur.com'

# FMS config info
# MONITOR_DEV = ['cpu', 'mem', 'disk', 'pcie', 'net', 'xfs', 'bmc', 'mpio', 'apei', 'lock', 'memt', 'loga', 'kernel']
MONITOR_DEV = ['cpu', 'mem', 'disk', 'pcie', 'net', 'xfs', 'bmc', 'lock', 'kernel', 'md']
DEV_SRC = ['srccpu', 'srcmem', 'srcdisk', 'srcpcie', 'srcnet', 'srcxfs', 'srcbmc', 'srclock', 'srckernel', 'srcmd']
CONSTR_AGENT = 'agent'
CONSTR_SRC = 'src'

# evt_level
CRITICAL = 'Critical'
MAJOR = 'Major'
MINOR = 'Minor'
TRIVIAL = 'Trivial'
LEVEL_LIST = [CRITICAL, MAJOR, MINOR, TRIVIAL]

# database
CPU_EVT_DB = 'CpuEvents'
MEM_EVT_DB = 'MenEvents'
DISK_EVT_DB = 'DiskEvents'
DATABASE_INFO = {
    'cpu': 'cpu_event',
    'mem': 'mem_event',
    'disk': 'disk_event',
    'pcie': 'pcie_event',
    'net': 'net_event',
    'xfs': 'xfs_event',
    'bmc': 'bmc_event',
    'lock': 'lock_event',
    'kernel': 'kernel_event',
    'md': 'md_event'
}
DEV_SO = {
    'cpu': 'cpumem',
    'mem': 'mem',
    'disk': 'disk',
    'pcie': 'pcie',
    'net': 'network',
    'xfs': 'xfs',
    'bmc': 'bmc',
    # 'mpio': 'mpio',
    # 'apei': 'apei',
    'lock': 'lock',
    # 'memt': 'mem-track',
    # 'loga': 'loganalyzer',
    'kernel': 'kern',
    'md': 'md'
}
DEV_SRC_DICT = {
    'srccpu': 'cpumem',
    'srcmem': 'mem',
    'srcdisk': 'disk',
    'srcpcie': 'pcie',
    'srcnet': 'network',
    'srcxfs': 'xfs',
    'srcbmc': 'bmc',
    # 'srcmpio': 'mpio',
    # 'srcapei': 'apei',
    'srclock': 'lock',
    # 'srcmemt': 'mem-track',
    # 'srcloga': 'loganalyzer',
    'srckernel': 'kern',
    'srcmd': 'md'
}

DEV_NAME = {
    'cpu': 'cpu',
    'mem': 'memory',
    'disk': 'disk',
    'pcie': 'pcie',
    'net': 'network',
    'xfs': 'xfs',
    'bmc': 'bmc',
    # 'mpio': 'mpio',
    # 'apei': 'apei',
    'lock': 'lock',
    # 'memt': 'mem-track',
    # 'loga': 'loganalyzer',
    'kernel': 'kernel',
    'md': 'md'
}

# query_type
QUERY_EVT = 'evt'
QUERY_DEV = 'dev'
QUERY_RECENT = 'recent'
QUERY_CPU = 'cpu'
QUERY_MEM = 'mem'
QUERY_DISK = 'disk'
QUERY_PCIE = 'pcie'
QUERY_NET = 'net'
QUERY_XFS = 'xfs'
QUERY_BMC = 'bmc'
QUERY_MPIO = 'mpio'
QUERY_APEI = 'apei'
QUERY_LOCK = 'lock'
QUERY_MEMT = 'memt'
QUERY_LOGA = 'loga'
QUERY_KERNEL = 'kernel'
QUERY_LIST = 'evtlist'
QUERY_REPAIR = 'repair'
QUERY_DEV_RECENT = 'devrecent'
QUERY_DEV_REPAIR = 'devrepair'
QUERY_DEV_REPAIRLIST = 'devreplist'
QUERY_MD = 'md'

# time
START_TIME = 'start'
END_TIME = 'end'
QUERY_CYCLE = 'cycle'

# config files
FAULT_ESC_PATH = '/usr/lib/fms/escdir/'
FAULT_PLUGINS_PATH = '/usr/lib/fms/plugins/'
FAULT_CPUMEM_ESC = 'cpumem.esc'
FAULT_DISK_ESC = 'disk.esc'
FAULT_CPUMEM_AGENT = 'cpumem_agent.conf'
FAULT_DISK_AGENT = 'disk_agent.conf'
FAULT_CPUMEM_SRC = 'cpumem_src.conf'
FAULT_DISK_SRC = 'disk_src.conf'
FAULT_CPUMEM_MOD = 'cpumem_agent_mod.conf'
FAULT_DISK_MOD = 'disk_agent_mod.conf'
FAULT_UPLOAD_PATH = '/usr/lib/fms/scripts/'
FAULT_SHELL_PATH = '/usr/lib/fms/shell/'
FAULT_CPU_SHELL = 'cpu_fault_new.sh'
FAULT_MEM_SHELL = 'memory_fault_new.sh'
FAULT_DISK_SHELL = 'disk_fault.sh'
ESC_FILE = '.esc'
AGENT_FILE = '_agent.conf'
SRC_FILE = '_src.conf'
MOD_FILE = '_agent_mod.conf'
SO_SRC = '_src.so'
SO_AGENT = '_agent.so'
HA_CONF_FILE = '/usr/lib/fms/ha/ha.conf'

# add fault
AGENT_KEYWD = 'subscribe'
SRC_KEYWD = 'interval'
MOD_KEYWD = 'event_handle_mode'

# fms commands
FMS_START = 'systemctl start fmd'
FMS_STOP = 'systemctl stop fmd'
FMS_MODINFO = 'fmsadm modinfo'
FMS_ADM_LOAD = 'fmsadm load'
FMS_ADM_UNLOAD = 'fmsadm unload'
FMS_ERR_DETAIL = 'err_detail'
FMS_STATUS = 'systemctl is-active fmd'
FMS_ACTIVE = 'active'
FMS_INACTIVE = 'inactive'

# monitor status
FMS_RUNNING = 'running'
FMS_DEAD = 'dead'
FMS_SERIOUS = 'serious'
FMS_SLIGHT = 'slight'

# other
FAULT_AUTO = 'auto'
FAULT_MANUAL = 'manual'
FAULT_SUCESS = 'sucess'
FAULT_FILE_FAIL = 'file data error!'
FAULT_FILE_UPLOAD_FAIL = 'file data error!'
FAULT_FILE_EXISTS = 'File already exists!'
FMS_CMD_ARGS_ERROR = 'args wrong!'
FAULT_ARGS_ERROR = 'args wrong!'
FAULT_FAIL = 'failed'
