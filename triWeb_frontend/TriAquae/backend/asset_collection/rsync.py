import multiprocessing
import sys,os,time
#sys.path.append('/root/py_training/py_web')
#os.environ['DJANGO_SETTINGS_MODULE'] ='settings'
#----------------Use Django Mysql model----------------
#import settings
#from  web01.models import IpMachine,IpGroup,HostLog
import MultiRunCounter
import db_connector
cur_dir = os.path.dirname(os.path.abspath(__file__))
sftp_script = 'python %s/multi_sftp.py' %cur_dir
ip = db_connector.IP.objects.filter(asset_collection=1)
ip_list = ''
for i in range(len(ip)):
    ip_list = ip_list + str(ip[i]) + ' '
#ip_list=sys.argv[1]
run_user='triaquae'
###send file to remote machine
option='-s'
file1='%s/collect.py' %cur_dir
file2='/tmp/collect.py'
task = '''%s '%s' %s %s %s %s''' % (sftp_script,ip_list,run_user,option,file1,file2)
print "\033[1;32;40m%s\033[0m" %'send file to remote machine!'
os.system(task)
###modify hardware collect script permit
cmd_script='python %s/multiprocessing_runCMD2.py' %cur_dir
option='--auto'
command='chmod 755 /tmp/collect.py'
task = '''%s %s '%s' '%s' %s''' % (cmd_script,option,ip_list,command,run_user)
print "\033[1;32;40m%s\033[0m" %'chown hardware collect script permit success'
os.system(task)
###run remote hardware collect python script
cmd_script='python %s/multiprocessing_runCMD2.py' %cur_dir
option='--auto'
command='sudo /tmp/collect.py'
task = '''%s %s '%s' '%s' %s''' % (cmd_script,option,ip_list,command,run_user)
print "\033[1;32;40m%s\033[0m" %'run remote hardware collect python script'
os.system(task)
###get file from remote machine
option='-g'
file1='/tmp/devinfo.txt'
file2='/root/devinfo.txt'
task = '''%s '%s' %s %s %s %s''' % (sftp_script,ip_list,run_user,option,file1,file2)
print "\033[1;32;40m%s\033[0m" %'get file from remote machine'
os.system(task)
###modify devinfo.txt user
cmd_script='python %s/multiprocessing_runCMD2.py' %cur_dir
option='--auto'
command='sudo chown %s:%s /tmp/devinfo.txt' %(run_user,run_user)
task = '''%s %s '%s' '%s' %s''' % (cmd_script,option,ip_list,command,run_user)
print "\033[1;32;40m%s\033[0m" %'modify /tmp/devinfo.txt user'
os.system(task)
###remove file in the remote machine
cmd_script='python %s/multiprocessing_runCMD2.py' %cur_dir
option='--auto'
command='rm -rf /tmp/devinfo.txt /tmp/collect.py'
task = '''%s %s '%s' '%s' %s''' % (cmd_script,option,ip_list,command,run_user)
print "\033[1;32;40m%s\033[0m" %'remove file in the remote machine'
os.system(task)
###wirte collect hardware information to mysql
write_script='python %s/write3.py' %cur_dir
task = '''%s''' % (write_script)
print "\033[1;32;40m%s\033[0m" %'wirte collect hardware information to mysql'
os.system(task)
