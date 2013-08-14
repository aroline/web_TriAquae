from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple 
from django.contrib.auth.models import User as djangouser, Group as djangogroup
from django.contrib.sites.models import Site as djangosite

import admin_ip

import logging.config, logging, logging.handlers

#self module
import models
import admin_ip, admin_user, admin_auth

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
logger = logging.getLogger(__name__)

#admin.site.unregister(djangouser)
#admin.site.unregister(djangogroup)
#admin.site.unregister(djangosite)

'''
class TriaquaeUserAdmin(admin.ModelAdmin):
    fields = ('user', 'email')
    filter_horizontal = ('remoteuser', 'ip')
'''




from models import OpsLogTemp,OpsLog,ServerStatus,AlertTemp


class LogAdmin(admin.ModelAdmin):
    list_display = ('user','ip','event_type','cmd','event_log','result','track_mark')

class OpsLogAdmin(admin.ModelAdmin):
    list_display = ('log_type','finish_date','log_type','tri_user','run_user','cmd','total_task','success_num','failed_num','track_mark','note')

class StatusAdmin(admin.ModelAdmin):
    search_fields = ('host','host_status')
    list_display = ('host','host_status','ping_status','availability','host_uptime','breakdown_count','up_count','attempt_count')

class AlertTempAdmin(admin.ModelAdmin):
    search_fields = ('host','snmp_status')
    list_display = ('host', 'snmp_data','snmp_status')


#admin.site.register(Idc, IdcAdmin)
admin.site.register(models.Idc)
admin.site.register(models.IP, admin_ip.IpAdmin)
admin.site.register(models.Group, admin_ip.GroupAdmin)
admin.site.register(models.RemoteUser, admin_user.RemoteUserAdmin)
admin.site.register(models.TriaquaeUser, admin_user.TriaquaeUserAdmin)
admin.site.register(models.AuthByIpAndRemoteUser, admin_auth.AuthByIpAndRemoteUserAdmin)
# added by Alex

admin.site.register(ServerStatus,StatusAdmin)
admin.site.register(OpsLogTemp,LogAdmin)
admin.site.register(OpsLog,OpsLogAdmin)
admin.site.register(AlertTemp,AlertTempAdmin)

