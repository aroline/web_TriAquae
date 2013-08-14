#!/usr/bin/env python

import sys,os,time

while True:
	os.system('python snmp_monitor.py -v 2c -c public -h localhost')
	
	time.sleep(50)
