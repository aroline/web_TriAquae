import multiprocessing
import sys,os,time
sys.path.append('/home/alex/Django-1.5/django/bin/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] ='mysite.settings'
#----------------Use Django Mysql model----------------
from mysite import settings
from  triWeb.models import IP,Group,HostLog
import MultiRunCounter

run_user = "MultiSftpTestUser"
track_num = MultiRunCounter.AddNumber()
script = 'python  ~/triWeb_dev/demo3_sftp.py'
ip_list = IP.objects.all()

host_list = sys.argv[1]
option= sys.argv[2]
file_name = sys.argv[3]

def compress(source_file):
	compressed_file = "%s.tgz" % source_file
	cmd = "tar cvzf %s %s" %(compressed_file,source_file)
	os.system(cmd)
	file_size = os.stat(compressed_file).st_size
	return compressed_file,file_size

if option == '-s':
	filename = compress(file_name)
	if  filename[1] > 10000000:
		size_in_MB = filename[1] / 1000000
		print 'The file afer compress is %sMB ,still bigger than our recommend 10MBs,transfer this file will cost quite long time,do you still want to transfer this file?' % size_in_MB

	else:
		print 'file size after compression is: %sbits ,will will start sending after 5 seconds!' % filename[1]
		time.sleep(5)
	new_filename = filename[0]
else:
	new_filename = file_name
# batch run process
result = []
def run(host):
	cmd = '''%s %s %s '%s' %s %s''' % (script,host,option,new_filename,track_num,run_user)
	os.system(cmd)

pool = multiprocessing.Pool(processes=20)

for ip in ip_list:
	result.append(pool.apply_async(run,(ip,)) )
#time.sleep(5)
#pool.terminate()

pool.close()
pool.join()


for res in result:
	res.get(timeout=5)
'''
else:
	reload(HostLog)
	
	HostLog.objects.filter(track_mark=track_num)
	print track_num	
	total = HostLog.objects.filter(track_mark=track_num)
	print total
	total_num = len(total)
	total_success =  len(total.filter(result = 'Success'))
	total_errors = len(total.filter(result = 'Error'))

	print 'Total: %s, success: %s , errors: %s ' % (total_num,total_success,total_errors)
'''
