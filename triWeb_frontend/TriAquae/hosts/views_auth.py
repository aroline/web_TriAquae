# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader, Context, RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import Context

#from unipath import Path
from triWeb import models
import datetime
import re, traceback

import logging.config, logging, logging.handlers
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
logger = logging.getLogger(__name__)

# buf format
# ip \t hostname \t idc \t protocol type \t port \t operating system
@csrf_protect
def load_batch_auth(request):
	if 'buf' in request.POST:
		buf = request.POST['buf']
		list_buf = buf.splitlines()
		num = 0
		for l in list_buf:
			l.strip()
			if re.match('#', l):  #filter comment lines
				continue
			logger.error('save %s' % l)
			try:
				(ip, remoteuser, authtype, password) = re.split('\s+', l)[:4]
				
				ip, created = models.IP.objects.get_or_create(ip=ip)
				logger.error('ip [%s] created[%s]' %(ip, created))
				remoteuser, created = models.RemoteUser.objects.get_or_create(name=remoteuser)
				logger.error('remoteuser [%s] created[%s]' %(remoteuser, created))
				obj_auth = models.AuthByIpAndRemoteUser(ip=ip, remoteUser=remoteuser, authtype=authtype, password=password)
				obj_auth.validate_unique()
				obj_auth.save()
				
				num += 1
			except:
				logger.error('%s' % traceback.format_exc())
		messages.info(request, 'load %s auths, filter %s ones' % (num, len(list_buf) - num))
		return  HttpResponseRedirect('/admin/triWeb/authbyipandremoteuser/')
	elif 'buf' in request.GET:
		logger.error(request.GET)
		return HttpResponseRedirect('/admin/triWeb/authbyipandremoteuser/')
		
@csrf_protect
def load_batch_auth_form(request):
	batch_title = 'load batch authorization'
	batch_comment = '\n#'.join(('', "Input your authorization for ip & remoteuser here. ",
					'Format: ip \t hostname \t IDC \t prototype \t port \t operating system. ', 
					'Example: ',
					'192.168.1.1 \t test1 \t BJ \t ssh-password \t 22 \t linux ',
					'192.168.1.2 \t test2 \t SH \t ssh-key \t 22 \t linux'))
	batch_context = {'batch_action':'/admin/triWeb/load_batch_auth/', 'batch_comment':batch_comment, 'batch_title':batch_title}
	return render(request, 'load_batch_form.html', batch_context)
