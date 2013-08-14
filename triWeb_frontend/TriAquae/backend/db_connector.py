#!/usr/bin/env python

import sys,os,time
sys.path.append('/usr/local/src/triWeb_frontend')
os.environ['DJANGO_SETTINGS_MODULE'] ='TriAquae.settings'
#----------------Use Django Mysql model----------------
from TriAquae.hosts.models import * 
#a =  OpsLog.objects.latest("track_mark").track_mark
