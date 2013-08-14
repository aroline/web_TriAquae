#!/usr/bin/env python
import sys,os
from datetime import *
#----------------Use Django Mysql model----------------

#from  triWeb.models  import IpMachine,Group,ConnectionMethod
import db_connector
#----------------Use Paramiko to connect ssh-----------

import paramiko
import logger
#print sys.argv

Split_line="------------- "

try:
	track_mark = sys.argv[4]
except IndexError:
	import MultiRunCounter
	track_mark = MultiRunCounter.AddNumber()

try:
	run_user = sys.argv[3]
except IndexError:
	run_user = "Tester_single"

h=db_connector.IpMachine.objects.get(ip = sys.argv[1])
host= h.ip 
port= int(h.port )
username = run_user 
password = db_connector.RemoteUser.objects.get(user_name=username).password
pkey_file = db_connector.RemoteUser.objects.get(user_name='root',description="test").RsaKey_file_path

cmd = sys.argv[2]


s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())


print h.protocol_type.protocol
try:
	if h.protocol_type.protocol == 'SSH_Key':
		#pkey_file = '/home/alex/.ssh/id_rsa'
		key = paramiko.RSAKey.from_private_key_file(pkey_file)
		s.connect(host,port,username,pkey=key,timeout=5)
		stdin,stdout,stderr = s.exec_command(cmd)
		#print Split_line,h.ip,Split_line

                result = stdout.read(),stderr.read()
                logger.RecordLog(host,'CommandExcution',cmd,result,'Success',track_mark,run_user)
		print Split_line,h.ip,Split_line,'\n',
		for line in result:
			print line,
		#print stderr.read()
	elif h.protocol_type.protocol == 'SSH':
		#try:
		s.connect(host,port,username,password,timeout=5)
        	stdin,stdout,stderr = s.exec_command(cmd)
		#print Split_line,h.ip,Split_line
        	result = stdout.read(),stderr.read()
		logger.RecordLog(host,'CommandExcution',cmd,result,'Success',track_mark,run_user)
		print Split_line,h.ip,Split_line,'\n',stdout.read()
        	if stderr.read():print 'error happend!',stderr.read()
                for line in result:
                        print line,
except paramiko.AuthenticationException:
	result =  host," ---Authentication failed!\n"
	print result
	logger.RecordLog(host,'CommandExcution',cmd,result,'Error',track_mark,run_user)
except :
	result =  host," ---timeout or configration error, please manually check the connection!\n"
	logger.RecordLog(host,'CommandExcution',cmd,result,'Error',track_mark,run_user)
	print result


#chan = s.invoke_shell()
#interactive.interactive_shell(chan)
#chan.close()


#stdin,stdout,stderr = s.exec_command(cmd)

s.close()
