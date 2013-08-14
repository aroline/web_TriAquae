# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader, Context, RequestContext
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template.loader import get_template
from django.template import Context

from triWeb import models
import datetime
import re, traceback

import logging.config, logging, logging.handlers
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
logger = logging.getLogger(__name__)

# buf format
# ip \t hostname \t idc \t protocol type \t port \t operating system
@csrf_protect
def load_batch_ip(request):
	if 'buf' in request.POST:
		buf = request.POST['buf']
		list_buf = buf.splitlines()
		num = 0
		for l in list_buf:
			if re.match('#', l):  #filter comment lines
				continue
			logger.error('save %s' % l)
			try:
				(ip, hostname, idc, protocol, port, os) = re.split('\s+', l)[:6]
				idc = models.Idc.objects.get(name=idc)
				models.IP(ip=ip, hostname=hostname, idc=idc, protocol = protocol, port =port, os=os).save()
				num += 1
			except:
				logger.error('%s' % traceback.format_exc())
		messages.info(request, 'load %s ips, filter %s lines' % (num, len(list_buf) - num))
		return  HttpResponseRedirect('/admin/triWeb/ip/')
	elif 'buf' in request.GET:
		logger.error(request.GET)
		messages.info(request, 'load 0 ips for http get ')
		return  HttpResponseRedirect('/admin/triWeb/ip/')
		
@csrf_protect
def load_batch_ip_form(request):
	return render(request, 'load_batch_ip_form.html')
