#!/usr/bin/env python
import os
import sys
import crypt
import subprocess
triaquae_user='triaquae'
hardware_script='collect.py'
save_dir='/tmp'
old_passwd='init'
###check run user 
if os.getuid() == 0:
    print "\033[1;32;40m%s\033[0m" %'This script run user is root!'
else:
    print "\033[1;31;40m%s\033[0m" %'This script must be run as root!'
    sys.exit(1)
###check python version
now_version=((sys.version).split()[0])[0:3]
require_version='2.6'
if now_version >= require_version:
    print "\033[1;32;40m%s\033[0m" %'Now python version is >2.6,pass!'
else:
    print "\033[1;31;40m%s\033[0m" %'Now python version is <2.6,not pass!'
###check install modules
modules=['subprocess','platform','json','crypt']
for i in modules:
    try:
        __import__(i)
    	print "\033[1;32;40m%s\033[0m" %'Now you system install require "%s" modules'%i
    except Exception,e:
	print "\033[1;31;40m%s\033[0m" %e
###check triaquae exist
triaquae_passwd=crypt.crypt(old_passwd,"TR")
cmd='useradd -p %s %s'%(triaquae_passwd,triaquae_user)
check_value=((subprocess.Popen("grep %s /etc/passwd|wc -l"%(triaquae_user),shell=True,stdout=subprocess.PIPE)).stdout.readline()).strip('\n')
if check_value == '1':
    print "\033[1;32;40m%s\033[0m" %'Triaquae user in the /etc/passwd!'
else:
    print "\033[1;31;40m%s\033[0m" %'Triaquae user not in the /etc/passwd!,now i will auto create'
    os.system(cmd)
###check triaquae user in sudoer
info='%s ALL=(root) NOPASSWD:ALL\n'%(triaquae_user)
f=open('/etc/sudoers','r')
if info in f.readlines():
    print "\033[1;32;40m%s\033[0m" %'Triaquae user in the /etc/sudoers!'
else:
    print "\033[1;31;40m%s\033[0m" %'Triaquae user not in the /etc/sudoers!'
    print  "\033[1;31;40m%s\033[0m" %'Please input "Triaquae ALL=(root) NOPASSWD:ALL" in the /etc/sudoers!'
f.close()
