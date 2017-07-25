# coding=utf-8
__author__ = 'shaomingwu@inspur.com'


# Define the constnt strings for error or warning messages.
DISK_FAILED_GETLIST = u"获取磁盘容量信息失败。"

# Define the pattern of the disk information.
DISK_INFO_PATTERN = r"^([\w-]+)\s+ ([\d.]+[\w]+)\s+(\w+)"

# define the keys for disk information.
DISK_KEY_LIST = "diskList"
DISK_KEY_NAME = "diskName"
DISK_KEY_CAP = "diskCap"
DISK_KEY_TYPE = "diskType"

# Define the command line for querying the disk information.
DISKINFO_CMDLINE = "lsblk -o NAME,SIZE,TYPE |grep disk"
