#from django.conf.urls import patterns, include, url
from django.conf.urls import *
from TriAquae.views import TriAquae
#from TriAquae.views import CpuUsage
#from TriAquae.views import ServiceStatus
#from TriAquae.datas import TriAquaeData
#from TriAquae.views import TriAquae, Command_Execution, File_Transfer, Server_Configuration, Job_Schedule, Assets_Management,GetServers
#from hosts.views import runCmd, cmd_result,AllUsers,AllCommands,stopExecution,getFailedLists,file_transfer,getFileLists,getDangerousCmd
from hosts.views import *

## Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TriAquae.views.home', name='home'),
    # url(r'^TriAquae/', include('TriAquae.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^admin/hosts/',include('TriAquae.hosts.admin_urls')),
    #url(r'^hosts/$',include('TriAquae.hosts.urls',namespace='hosts')),
    #url(r'^hosts/$',include('TriAquae.hosts.urls')),

    # start by zp
    url(r'^assets_management/$',assets),
    url(r'^assets_management/(?P<id>\d+)/$', assets_detail, name='assets_detail'),
    url(r'^assets_management/diff$',assets_diff),
    url(r'^server_status/$',status),
    url(r'^server_status/(?P<hostname>\S+)/$',status_detail, name='status_detail'),
    url(r'^command_execution$',command_execution),
    url(r'^file_transfer$',file_transfer),
    # end by zp

    #start by tangjing
    (r'^GetServers$',GetServers),
    (r'^runCmd/$',runCmd),
    (r'^cmd_result/$',cmd_result),
    (r'^AllCommands/$',AllCommands),
    (r'^AllUsers/$',AllUsers),
    (r'^stopExecution/$',stopExecution),
    (r'^getFailedLists/$',getFailedLists),
    (r'^transferFile/$',transfer_file),
    (r'^getFileLists/$',getFileLists),
    (r'^getDangerousCmd/$',getDangerousCmd),
    #(r'^loadFileTransferPage/$',loadFileTransferPage),
    #end by tangjing
)
