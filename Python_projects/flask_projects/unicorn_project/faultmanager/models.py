from django.db import models


# Create your models here.
class MemEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'mem_event'


class CpuEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'cpu_event'


class DiskEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'disk_event'


class RepEvents(models.Model):

    device_name = models.TextField()
    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp_rep = models.TextField()
    timestamp_1 = models.TextField()
    timestamp_2 = models.TextField()
    err_type = models.TextField()
    err_msg = models.TextField()
    action = models.TextField()
    err_count = models.IntegerField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()

    class Meta:

        db_table = 'rep_event'


class PcieEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'pcie_event'


class NetEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'net_event'


class XfsEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'xfs_event'


class BmcEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'bmc_event'


class MpioEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'mpio_event'


class ApeiEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'apei_event'


class LockEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'lock_event'


class MemtEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'memt_event'


class LogaEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'loga_event'


class KdumpEvents(models.Model):

    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:

        db_table = 'kernel_event'


class MdEvents(models.Model):
    year = models.TextField()
    month = models.TextField()
    day = models.TextField()
    timestamp = models.TextField()
    err_msg = models.TextField()
    err_type = models.TextField()
    dev_id = models.IntegerField()
    evt_id = models.IntegerField()
    detail = models.TextField()
    evt_level = models.TextField()

    class Meta:
        db_table = 'md_event'


class DevScore(models.Model):
    dev_name = models.TextField()
    score = models.IntegerField()

    class Meta:
        db_table = 'dev_score'


class DevStatus(models.Model):
    dev_name = models.TextField()
    status = models.TextField()

    class Meta:
        db_table = 'dev_status'


class Email(models.Model):
    email = models.TextField()
    status = models.TextField()

    class Meta:
        db_table = 'email'
#
#
# class Ha(models.Model):
#     name_node = models.TextField()
#     role = models.TextField()
#     ip_addr = models.TextField()
#     port = models.IntegerField()
#     status = models.TextField()
#
#     class Meta:
#         db_table = 'ha'
#
#
# class Module(models.Model):
#
#     name = models.TextField()
#
#     class Meta:
#
#         db_table = 'module'
