# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader, Context, RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import Context

#3rd module
import datetime
import re, traceback
from collections import defaultdict
#self module
from triWeb import models


import logging.config, logging, logging.handlers
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
logger = logging.getLogger(__name__)

# buf format
# ip \t hostname \t idc \t protocol type \t port \t operating system
@csrf_protect
def load_batch_remoteuser(request):
	if 'buf' in request.POST:
		buf = request.POST['buf']
		list_buf = [l.strip() for l in buf.splitlines() if l.strip()]
		num = 0
		dict_triaquaeuser = defaultdict(set)
		for l in list_buf:
			try:
				if re.match('#', l):  #filter comment lines
					continue
				logger.error('save %s' % l)
				(remoteuser, triaquaeuser) = re.split('\s+', l)[:2]
				dict_triaquaeuser[triaquaeuser].add(remoteuser)
			except:
				logger.error('%s\t[%s]' % (l, traceback.format_exc()))
				
		for t in dict_triaquaeuser:
			try:
				tuser = models.TriaquaeUser.objects.get(user__username__exact=t)
				for r in dict_triaquaeuser[t]:
						remoteuser,create = models.RemoteUser.objects.get_or_create(name__exact=r)
						logger.error('user [%s] remoteuser [%s]' % (tuser, remoteuser))
						remoteuser.save()
						tuser.remoteuser.add(remoteuser)
						num += 1
			except:
				logger.error('%s' % traceback.format_exc())
		messages.info(request, 'load %s auths, filter %s ones' % (num, len(list_buf) - num))
		return  HttpResponseRedirect('/admin/triWeb/remoteuser/')
	elif 'buf' in request.GET:
		logger.error(request.GET)
		return HttpResponseRedirect('/admin/triWeb/remoteuser/')
		
@csrf_protect
def load_batch_remoteuser_form(request):
	batch_title = 'load batch remoteuser'
	batch_comment = '\n#'.join(('', "Input your remoteuser with users here. ",
					'Format: remoteuser \t user. ', 
					'Example: ',
					'test \t tom',
					'weblogic \t jerry'))
	batch_context = {'batch_action':'/admin/triWeb/load_batch_remoteuser/', 'batch_comment':batch_comment, 'batch_title':batch_title}
	return render(request, 'load_batch_form.html', batch_context)
