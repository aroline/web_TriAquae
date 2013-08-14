from django.db import models
from django import forms
from datetime import datetime

from django.contrib.auth.models import (User, BaseUserManager, AbstractBaseUser)
# Create your models here.


class Idc(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class IP(models.Model):
    hostname=models.CharField(max_length=50, unique=True)
    ip = models.IPAddressField(unique=True)
    idc = models.ForeignKey(Idc, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    #PROTOCOL_CHOICES = (('ssh', 'ssh-password'), ('ssh-key','ssh-key'))
    #protocol = models.CharField(max_length=20, default='ssh', choices=PROTOCOL_CHOICES, verbose_name='Protocol type')
    port = models.IntegerField(default='22')
    os = models.CharField(max_length=20, default='linux', verbose_name='Operating System')
    
    #snmp related
    alert_limit = models.IntegerField(default=5)
    snmp_alert_limit = models.IntegerField(default=5)
    asset_collection = models.BooleanField(default=True,verbose_name='enable asset collection')
    snmp_on = models.BooleanField(default=True)
    snmp_version = models.CharField(max_length=10,default='2c')
    snmp_community_name = models.CharField(max_length=50,default='public')
    snmp_security_level = models.CharField(max_length=50,default='auth')
    snmp_auth_protocol = models.CharField(max_length=50,default='MD5')
    snmp_user = models.CharField(max_length=50,default='triaquae_snmp')
    snmp_pass = models.CharField(max_length=50,default='my_pass')

    system_load_warning = models.IntegerField(default=0,blank=True,verbose_name="load >")
    system_load_critical = models.IntegerField(default=0,blank=True)
    cpu_idle_warning = models.IntegerField(default=0,blank=True, verbose_name = "cpuIdle% < ")
    cpu_idle_critical= models.IntegerField(default=0,blank=True)
    mem_usage_warning = models.IntegerField(default=0,blank=True, verbose_name="memoryUsage% >")
    mem_usage_critical = models.IntegerField(default=0,blank=True)
    def __unicode__(self):
        return self.ip
    '''
    def save(self):
        pass
    '''
class RemoteUser(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    def __unicode__(self):
        return self.name

class TriaquaeUser(models.Model):
    user = models.ForeignKey(User, null=True)
    email = models.EmailField()
    remoteuser = models.ManyToManyField(RemoteUser, null=True, blank=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    ip = models.ManyToManyField(IP, null=True, blank=True)
    def __unicode__(self):
        return '%s' % self.user

class AuthByIpAndRemoteUser(models.Model):
    password = models.CharField(max_length=1024,verbose_name="Password or SSH_KEY")
    AUTH_CHOICES = (('ssh', 'ssh-password'),('ssh-key', 'ssh-key'))
    authtype = models.CharField(max_length=100, choices=AUTH_CHOICES)
    ip = models.ForeignKey(IP, null=True, blank=True)
    remoteUser = models.ForeignKey(RemoteUser, null=True, blank=True)
    def __unicode__(self):
        return '%s\t%s' % (self.ip, self.remoteUser)
    #save throw exception
    class Meta:
        unique_together = (('ip','remoteUser'),)
        


class ServerStatus(models.Model):
    host = models.IPAddressField(primary_key=True)
    host_status = models.CharField(max_length=10,default='Unkown')
    ping_status = models.CharField(max_length=100,default='Unkown')
    last_check = models.DateTimeField(auto_now_add=True)
    host_uptime = models.CharField(max_length=50,default='Unkown')
    attempt_count = models.IntegerField(default=0)
    breakdown_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    snmp_alert_count = models.IntegerField(default=0)
    availability = models.CharField(max_length=20,default=0)
    def __unicode__(self):
        return self.host
                
class AlertTemp(models.Model):
    host = models.IPAddressField(primary_key=True)
    snmp_status = models.CharField(max_length=20)
    snmp_data  = models.CharField(max_length=200)
    
class OpsLog(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(null=True,blank=True)
    log_type = models.CharField(max_length=50)
    tri_user = models.CharField(max_length=30)
    run_user = models.CharField(max_length=30)
    cmd = models.TextField()
    total_task = models.IntegerField()
    success_num = models.IntegerField()
    failed_num = models.IntegerField()
    track_mark = models.IntegerField(unique=True)
    note = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return self.cmd

class OpsLogTemp(models.Model):
        date = models.DateTimeField(auto_now_add=True)
        user = models.CharField(max_length=30)
        ip = models.IPAddressField()
        event_type = models.CharField(max_length=50)
        cmd = models.TextField()
        event_log = models.TextField()
        result = models.CharField(max_length=30,default='unknown')
        track_mark = models.IntegerField(blank=True)
        note = models.CharField(max_length=100,blank=True)
        def __unicode__(self):
            return self.ip
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Hosts(models.Model):
    host = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    alias = models.CharField(max_length=64, null=True)
    group = models.CharField(max_length=64, null=True)
    platform = models.CharField(max_length=64)
    platform_full = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=64, null=True)
    hw_cpu = models.CharField(max_length=255, null=True)
    hw_memory = models.CharField(max_length=64, null=True)
    macaddress_a = models.CharField(max_length=64, null=True)
    macaddress_b = models.CharField(max_length=64, null=True)
    hw_full = models.TextField(null=True)
    location = models.CharField(max_length=255, null=True)
    vendor = models.CharField(max_length=64, null=True)
    supplier = models.CharField(max_length=64, null=True)
    contract_number = models.CharField(max_length=64, null=True)
    purchase_date = models.DateField('purchase date', null=True)
    expiry_date = models.DateField('expiry date', null=True)
    serialno_a = models.CharField(max_length=64, null=True)
    serialno_b = models.CharField(max_length=64, null=True)
    tag = models.CharField(max_length=64, null=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return self.name

