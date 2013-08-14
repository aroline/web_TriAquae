#!/usr/bin/env python

import sys,os,time
#sys.path.append('/usr/local/src/triWeb_frontend/TriAquae')
sys.path.append('/wrk/sysadmin/arolinez/web/git/web_TriAquae/triWeb_frontend/')
os.environ['DJANGO_SETTINGS_MODULE'] ='TriAquae.settings'
#----------------Use Django Mysql model----------------
#import settings
#from host.models import *


#from django.conf import settings
from TriAquae.host.models import *
#from host.models import *

