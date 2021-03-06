#!/usr/bin/env python

import multiprocessing
import sys,os,time,subprocess
import db_connector,logger,MultiRunCounter
import tri_config
#----------------Use Django Mysql model----------------

cur_dir = os.path.dirname(os.path.abspath(__file__))
script = '%s/snmp_monitor.py' % cur_dir
print script

snmp_result_dic = {}

date2 =time.strftime('%Y_%m_%d %H\:%M\:%S')
print date2

#sys.exit()
if __name__ == "__main__":
	ip_list = db_connector.IP.objects.filter(snmp_on = 'YES' ) 	
	result = []
	def run(host,snmp_version,comm_name, security_level, auth_protocol, snmp_user, snmp_pass):
		if snmp_version == '2c':
			cmd_result = os.popen('python %s -v %s -c %s -h %s' %(script, snmp_version, comm_name, host)).read()
		if snmp_version == '3':
			cmd_result = os.popen('python %s -v %s -u %s -l %s -a %s -A %s -h %s' %(script, snmp_version, snmp_user, security_level, auth_protocol, snmp_pass, host) ) 
		snmp_result_dic[host] = cmd_result
	while True:
		os.system('> %s' % tri_config.Snmp_temp_log)
		#db_connector.AlertTemp.objects.all().delete()
		if len(ip_list) < 100:
			thread_num = len(ip_list)
		else:
			thread_num = 100
		pool = multiprocessing.Pool(processes=thread_num)
		
		for ip in ip_list:
			snmp_version = ip.snmp_version
			comm_name = ip.snmp_community_name
			security_level = ip.snmp_security_level
			auth_protocol = ip.snmp_auth_protocol
			snmp_user = ip.snmp_user
			snmp_pass = ip.snmp_pass
			cmd_argvs = ()	
			result.append(pool.apply_async(run,(ip,snmp_version,comm_name, security_level, auth_protocol, snmp_user, snmp_pass)) )

		pool.close()
		pool.join()


		for res in result:
			res.get(timeout=5)
		print 'sleep 300 seconds.....'
		time.sleep(300)

	print snmp_result_dic
