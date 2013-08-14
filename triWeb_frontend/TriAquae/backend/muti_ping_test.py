import os,sys
import time
import subprocess
from subprocess import Popen
#------------
###################-------------------------------
import db_connector
#ip_list = db_connector.IpMachine.objects.filter(ip__startswith='10.98.33.')
ip_list = db_connector.IpMachine.objects.all()
ping_status_dic = {}
ping_error_list = []
p = [] # ip -> process
#for i in ip_list:
for i in ip_list:
	#ip = "10.98.33.%s" % i
	ip = i.ip
	if len(db_connector.ServerStatus.objects.filter(host = ip)) ==0:
		insert_status_item = db_connector.ServerStatus.objects.create(host = ip)
		insert_status_item.save()
	p.append((ip, Popen(['ping', '-c', '3', ip], stdout=subprocess.PIPE)))

while p:
    for i, (ip, proc) in enumerate(p[:]):
        if proc.poll() is not None: # ping finished
            p.remove((ip, proc)) # this makes it O(n**2)
            #ping_status_dic[ip] = proc.communicate() # add result to dic
	    #print proc.returncode
	    if proc.returncode != 0: #error 
		ping_error_list.append(ip)
	    else:
                ping_status_dic[ip] = proc.communicate() # add result to dic
		

for ip,result in ping_status_dic.items():
	status = result[0].split('received,')[1].split('%')[0].strip()
	if 'rtt' in result[0]: # normal
		rtt = result[0].split('\n')[-2]
		print ip,status,rtt
		ok_ip = db_connector.ServerStatus.objects.get(host=ip)
		ok_ip.ping_status = rtt
		ok_ip.host_status = 'UP'
		ok_ip.save()
	elif 'error' in status:   #unreachable
		
		print ip,'err',status.split()[-1]

	else:   # 
		print ip,'---->packet loss',status

#--------------------------- 
# ping doesn't work ,use nc to scan port 

#for ip in ping_error_list:
#	print ip,'error'

#print "\033[32;1m Ok: %s , unreachable:%s\033[0m" %(len(ping_status_dic),len(ping_error_list))


T = []
Port_status_dic = {}
if len(ping_error_list) > 0:
	for i in ping_error_list:
		ip = "%s" % i
        	T.append((ip, Popen(['nc', '-w', '1', ip,'22'], stdout=subprocess.PIPE)))
	
	while T:
		for i, (ip,proc) in enumerate(T[:]):
			if proc.poll() is not None:
				T.remove((ip,proc))
				if proc.returncode == 0:
					Port_status_dic[ip] = 'YES'
				else:
					Port_status_dic[ip] = 'NO'
	#time.sleep(.04)

	if Port_status_dic:
		for err_ip,port_status in Port_status_dic.items():
			ip = db_connector.ServerStatus.objects.get(host= err_ip)
			msg= "Ping doesn't work. Telnet port:22 Reachable: %s" % port_status
			ip.ping_status = msg
			if port_status == 'NO':
				ip.host_status = 'DOWN'
			else:
				ip.host_status = 'UP'
			ip.save()
			
#for ip in ping_error_list:
#       print ip,'error'

print "\033[32;1m Ok: %s , unreachable:%s\033[0m" %(len(ping_status_dic),len(ping_error_list))

