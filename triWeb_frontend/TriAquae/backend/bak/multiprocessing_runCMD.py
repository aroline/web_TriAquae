#!/usr/bin/env python
import multiprocessing
import sys,os,time
import db_connector
#----------------Use Django Mysql model----------------

cur_dir = os.path.dirname(os.path.abspath(__file__))
script = 'python %s/run_command3.py' % cur_dir

try:
	if sys.argv[1] == '-h':
		print '''\n\033[32;1mUsage: python multiprocessing_runCMD.py 'ip_list' cmd run_user track_num\033[0m
Example: python multiprocessing_runCMD.py '192.168.2.13 202.106.0.23 10.0.0.2' 'df -h' alex 34 \n'''
		sys.exit()
except IndexError:
	print "Usage: python multiprocessing_runCMD.py 'ip_list' cmd run_user track_num"
	sys.exit()
try:
	track_num = sys.argv[4]
except IndexError:
	import MultiRunCounter
	track_num = MultiRunCounter.AddNumber()
'''
try:
	print 'track_mark:',track_num
	last_run_track_mark = int(track_num) - 1
	os.rename('operation.log','track_id_%s_operation.log' % last_run_track_mark)
except OSError:
	pass

'''	
if __name__ == "__main__":
	run_user = sys.argv[3] 
	#ip_list = db_connector.IP.objects.all()
	
	raw_ip_list = sys.argv[1].split()
	remove_duplicate_ip = set(raw_ip_list)
	ip_list = list(remove_duplicate_ip)
	#host_list = sys.argv[1]
	cmd= sys.argv[2]
	#run_user = sys.argv[3]

	# batch run process
	result = []
	def run(host):
		task = '''%s %s '%s' %s %s''' % (script,host,cmd,run_user,track_num)
		os.system(task)

	if len(ip_list) < 50:
		thread_num = len(ip_list)
	else:
		thread_num = 50
	pool = multiprocessing.Pool(processes=thread_num)

	for ip in ip_list:
		result.append(pool.apply_async(run,(ip,)) )
	#time.sleep(5)
	#pool.terminate()

	pool.close()
	pool.join()


	for res in result:
		res.get(timeout=5)
