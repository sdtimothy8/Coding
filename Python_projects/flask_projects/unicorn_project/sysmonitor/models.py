"""
models for module sysmonitor
"""
from django.db import models


# Create your models here.
class MemBasicInfo(models.Model):
    """
    table for MemBasicInfo
    """
    percent = models.FloatField(max_length=5)


class CpuLoadBasicInfo(models.Model):
    """
    table for CpuLoadBasicInfo
    """
    oneminute = models.FloatField(max_length=15)
    fiveminute = models.FloatField(max_length=15)
    fifteenminute = models.FloatField(max_length=15)


class DiskioBasicInfo(models.Model):
    """
    table for CpuLoadBasicInfo
    """
    tpsnum = models.FloatField(max_length=15)
