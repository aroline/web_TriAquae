from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib import auth

from models import Devinfo, Check_Devinfo, ServerStatus, DevForm
from models import Group,IP,RemoteUser,OpsLog,OpsLogTemp
#from models import *

from TriAquae.backend import MultiRunCounter
#from backend import MultiRunCounter

import datetime, os, time
import json

#start by zp
yesterday = (datetime.datetime.now()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")

def assets(request):
    latest_host_list = Devinfo.objects.order_by('-id')
    auto_check  = Check_Devinfo.objects.filter(Change_Time__gte=yesterday, Change_Time__lte=datetime.date.today()).count()
    #auto_check  = '2'
    context = { 'latest_host_list':latest_host_list, 'auto_check':auto_check }
    return render(request, 'assets_management.html', context)

def assets_detail(request, id):
    host = Devinfo.objects.get(pk=id)
    form = DevForm(instance=host)
    return render(request, 'assets_detail.html', {'host':host, 'form':form}, context_instance=RequestContext(request))

def assets_diff(request):
    latest_host_list = Check_Devinfo.objects.filter(Change_Time__gte=yesterday, Change_Time__lte=datetime.date.today())
    context = { 'latest_host_list':latest_host_list }
    return render(request, 'assets_diff.html', context)

def status(request):
    latest_host_list = ServerStatus.objects.all()
    context = { 'latest_host_list':latest_host_list }
    return render(request, 'server_status.html', context)

def status_detail(request,hostname):
    host = ServerStatus.objects.get(hostname=hostname)
    assets = Devinfo.objects.get(System_Hostname=hostname)
    return render(request, 'status_detail.html', {'host':host, 'assets':assets}, context_instance=RequestContext(request))

#end by zp

#start by tangjing

def command_execution(request):
    t = get_template('command_execution.html')
    #html=t.render(Context({'form_name':'Enter your command:'}))
    html=t.render(Context())
    return HttpResponse(html)


def file_transfer(request):
    t = get_template('file_transfer.html')
    html=t.render(Context())
    return HttpResponse(html)

def GetServers(request):
    data = []
    counter = 0
    group_list  = Group.objects.all()
    for g_name in group_list:
        counter += 1
        data.append({'id': counter, 'pid':0, 'text':g_name.name, 'bgroup':1})
        ip_list =  IP.objects.filter(group__name = g_name.name)
        ip_counter = 0
        for ip in ip_list:
            ip_counter += 1
            data.append({'id':'%s%s'%(counter,ip_counter), 'pid': counter, 'text':ip.hostname,       'bgroup':0 , 'ip':ip.ip })

        '''data=[
         { 'id':1,'pid':0, 'text': 'Node 1','bgroup':1},
         { 'id':11,'pid':1, 'text': 'Node 1.1','bgroup':0},
         { 'id':12,'pid':1, 'text': 'Node 1.2','bgroup':0},
         { 'id':2,'pid':0,'text': 'Node 2' ,'bgroup':0},
         { 'id':3,'pid':0,'text': 'Node 3' ,'bgroup':0},
         { 'id':4,'pid':0,'text': 'Node 4' ,'bgroup':0},
         { 'id':5,'pid':0,'text': 'Node 5' ,'bgroup':0},
         ];'''
        #data=[{'a':'b'}]
        return HttpResponse(json.dumps(data));





def login(request):
	return render_to_response('login.html')
def account_login(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username,password=password)
	if user is not None: #and user.is_active:
		#correct password and user is marked "active"
		auth.login(request,user)
		return HttpResponseRedirect("/hello/")
	else:
		return render_to_response('login.html',{'login_err':'Wrong username or password!'})

def logout_view(request):
    user = request.user
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponse("%s logged out!" % user)
def hello(request):
  if request.user.is_authenticated() is None:
	return HttpResponse("User not login yet!!!")
  else:

	now = datetime.datetime.now()
	group_list ={}
	for group in Group.objects.all():
		ip_nums_in_group = IP.objects.filter(group__group_name = group)
		group_list[group] = ip_nums_in_group

	return render_to_response("boot1.html",{'group_list':group_list, 'user':request.user})
	#return render_to_response('hello.html',{'current_date': now} )

def batch_management(request):
  if request.user.is_authenticated() is None:
        return HttpResponse("User not login yet!!!")
  else:

        now = datetime.datetime.now()
        group_list ={}
        for group in Group.objects.all():
                ip_nums_in_group = IP.objects.filter(group__group_name = group)
                group_list[group] = ip_nums_in_group
	RemoteUsers = RemoteUser.objects.all()
	return render_to_response("BatchManagement.html",{'group_list':group_list, 'user':request.user,'r_users':RemoteUsers})
#return HttpResponse('{"success_tasks":%s,"failed_tasks":%s,"cmd_log":[%s]}' %(success_tasks,failed_tasks,cmd_ret))

def cmd_result(request):
                track_id = request.GET['TrackMark']
                total_tasks = request.GET['TotalTasks']
                success_tasks= OpsLog.objects.get(track_mark = track_id).success_num
                failed_tasks = OpsLog.objects.get(track_mark = track_id).failed_num

		command_result = OpsLogTemp.objects.filter(track_mark = track_id)
		data_dic = {}
		for ip in command_result:
			data_dic[ip.ip] = [ip.ip, ip.user,  ip.event_log,  ip.result, ip.note ]

		data_dic['result_count'] = [success_tasks, failed_tasks]
        	return HttpResponse(json.dumps(data_dic))

def get_groupList(request):
	if request.is_ajax():
	        #if request_method == "GET":
		G_name = request.GET['Name']
		ip_list = IP.objects.filter(group__group_name = G_name)

	return render_to_response('server_list.html',{"ip_list_of_group":ip_list},context_instance=RequestContext(request))


def runCmd(request):
    track_mark = MultiRunCounter.AddNumber()
    user_input = request.POST['command']
    user_account = request.POST['UserName']
    iplists = request.POST['IPLists'].split(',')

    task_num = len(iplists)
    print "user inputs command is: %s and username is:%s and iplists are: %s" %(user_input,user_account,' '.join(iplists))
    #cmd = "python /usr/local/src/triWeb_frontend/TriAquae/backend/multiprocessing_runCMD2 '%s' '%s' alex %s %s &" % (ip_list_to_string,user_input,track_mark,os.listdir('.'))
    cmd = "python /usr/local/src/triWeb_frontend/TriAquae/backend/multiprocessing_runCMD2.py %s '%s' '%s' alex &" % (track_mark,' '.join(iplists),user_input)
    os.system(cmd)
    return HttpResponse('{"TrackMark":%s, "TotalNum":%s}' %(track_mark, task_num))
def getFailedLists(request):
	track_id = request.GET['TrackMark']
	fail_list = OpsLogTemp.objects.filter(track_mark = track_id,result ="Error")
	ip_list = []
	for ip in fail_list:
		ip_list.append(ip.ip)
        return HttpResponse(json.dumps(ip_list))
def AllUsers(request):
	#loginuser = request.GET['LoginUser']
	user_list =RemoteUser.objects.all()
	u_list = []
	for user in user_list:
		u_list.append(user.name)
	return HttpResponse(json.dumps(u_list))
def AllCommands(request):
	#allcommands = ["df","iostat","shutdown","restart"]
	#return HttpResponse('["df","iostat","shutdown","restart"]')
        cmd_list = os.popen('bash /usr/local/src/triWeb_frontend/TriAquae/backend/command_list.sh').read()
        #commands = cmd_list.split('\n')
	print cmd_list
        return HttpResponse(cmd_list)
def stopExecution(request):
	trackmark = request.GET['TrackMark']
	#todo
	cmd = '''ps -ef |grep -v grep |grep "multiprocessing_runCMD2.py %s" |awk '{print $2}'|xargs kill -9''' % trackmark
	print cmd
	os.system(cmd)
	return HttpResponse("stop successfully")
def getFileLists(request):
	SftpSendDir = '/tmp/TriFTP'

	file_list = os.listdir(SftpSendDir)
	list_dic = {}
	for f in file_list:
		if os.path.isdir('%s/%s' %(SftpSendDir,f))  is True:
			d = os.popen('du -sh %s/%s ' %(SftpSendDir,f))
			f_size = d.read().split('\t')[0]
			f_type = 'dir'
			list_dic[f] = [f_size,f_type]
		else:
			f_size ='%sBit'% os.lstat('%s/%s' %(SftpSendDir,f)).st_size
			f_type = 'file'
			list_dic[f] = [f_size,f_type]

	#return HttpResponse('["hhhhhhhhhhhhhhhhhhhhhhhhkkkkkkkkkkkkkhh","ii"]')
	return HttpResponse(json.dumps(list_dic))

def transfer_file(request):
	ip_list = request.POST['IPLists'].split(',')
	print ip_list
	ip_list_to_string = ' '.join(ip_list)
	print ip_list_to_string
	option = request.POST['command']
	remote_user = request.POST['UserName']
	track_mark = MultiRunCounter.AddNumber()
	if option == 'SendFile':
		local_path = "/tmp/TriFTP/"
	        file_list = request.POST['FileLists'].split(',')
		print file_list
		remote_path = request.POST['RemotePath']
		def compress(source_file_list):
			format_file_list = []
			for f in source_file_list:
				format_file_list.append('%s%s' %(local_path,f))
			file_list_to_string = ' '.join(format_file_list)
			compressed_file = time.strftime('TriSFTP_send_file_%Y%m%d_%H_%M_%S.tgz')
			cmd = "tar cvzf %s %s" %(compressed_file,file_list_to_string)
			os.system(cmd)
			file_size = os.stat(compressed_file).st_size
			return compressed_file
		transfer_action = "python  /usr/local/src/triWeb_frontend/TriAquae/backend/multiprocessing_sftp2.py %s %s -s %s %s '%s' &" %(track_mark,remote_user,compress(file_list),remote_path,ip_list_to_string)
	elif option == 'GetFile':
		local_path = '/tmp/TriFTP/Recv/'
		remote_file = request.POST['RemotePath']
		transfer_action = "python  /usr/local/src/triWeb_frontend/TriAquae/backend/multiprocessing_sftp2.py %s %s -g %s '%s' &" %(track_mark,remote_user,remote_file,ip_list_to_string)

	os.system(transfer_action)
	total_task = len(ip_list)
        return HttpResponse('{"TrackMark":%s, "TotalNum":%s}' %(track_mark,total_task))
	#return HttpResponse("%s, %s" %(total_task, track_mark))
def getDangerousCmd(request):
	dangerous_filename = '/usr/local/src/triWeb_frontend/TriAquae/backend/dangerous_cmd.txt'
	f= file(dangerous_filename)
	cmd_list = f.read().split('\r\n')
	print cmd_list
	return HttpResponse(json.dumps(cmd_list))
