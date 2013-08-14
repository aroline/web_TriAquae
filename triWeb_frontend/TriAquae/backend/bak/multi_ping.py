#!/usr/bin/env python
import multiprocessing
import sys,os,subprocess,time
import db_connector
#----------------Use Django Mysql model----------------

cur_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
	
	# batch run process
	result = []
	def run(host,status,error_list):
		proc = subprocess.Popen(['ping', '-c', '3', host], stdout=subprocess.PIPE)
		while True:
		  if proc.poll() is not None: # ping finished
                	if proc.returncode != 0: #PING error 
				print proc.returncode
                        	error_list.append(host) # add error ip to list 
                	else:
                        	# add result to dic
				status[host] = proc.communicate()
                	break
	#if len(ip_list) < 50:
	#	thread_num = len(ip_list)
	#else:
	thread_num =100 
	pool = multiprocessing.Pool(processes=thread_num)

	manager = multiprocessing.Manager()
	server_status_dic = manager.dict()  # set up a dic for process to call 
	ping_error_list = manager.list()

	for i in range(1,254):
		
		ip = "10.98.33.%s" % i
		result.append(pool.apply_async(run,(ip,server_status_dic,ping_error_list)) )
	#time.sleep(5)
	#pool.terminate()

	pool.close()
	pool.join()
	#for k,v in server_status_dic.items():
	#	print k,v 
	print 'error_nums',len(ping_error_list),'ok_nums',len(server_status_dic)
	#for res in result:
	#	res.get(timeout=5)
