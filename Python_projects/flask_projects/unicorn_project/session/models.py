from django.db import models


class Auths(models.Model):
    authcode = models.CharField(primary_key=True, max_length=32)
    access_time = models.DecimalField(max_digits=20, decimal_places=6)


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=32)
    access_time = models.DecimalField(max_digits=20, decimal_places=6)
    try_times = models.IntegerField()
