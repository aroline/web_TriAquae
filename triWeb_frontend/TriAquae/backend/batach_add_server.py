#!/usr/bin/env python
import db_connector

g_name = db_connector.Group.objects.get(name ='SH')

for i in range(1,254):
	addr = '10.98.33.%s' % i
	add_server = db_connector.IP.objects.create(

	ip = addr, 
	hostname = "Test_server_%s" % addr,
	port = 22,
	os =  'Linux test',
	#group = g_name,

	)	

	add_server.group.add(g_name)


