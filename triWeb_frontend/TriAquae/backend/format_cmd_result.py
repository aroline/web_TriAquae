#!/usr/bin/env python

import db_connector


h = db_connector.OpsLogTemp.objects.filter(track_mark=279)

#l = h[1].event_log

#e = l.encode('utf-8')
#for line in e.split('\\n'):
#	print line

'''f = file('cmd.log','w')
for line in h:
	f.write('%s	%s	%s	%s\n' % (line.ip.encode('utf-8'),line.track_mark,line.cmd,line.result))
	cmd_result = line.event_log
	format_result = cmd_result.encode('utf-8')
	for i in format_result.split('\\n'):
		f.write('%s\n' %i)

'''

for ip in h:
	results = ip.event_log
	r2 = results.split('\\n')
	for line in r2:
		print line
