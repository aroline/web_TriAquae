web_TriAquae
============

This is web TriAquae.

config steps:

step1:

git clone git@github.com:aroline/web_TriAquae.git

put triWeb_frontend into /usr/local/src, it will looks like /usr/local/src/triWeb_frontend

step2:
create a database named TriAquae.
modify your mysql accounts in the setting.py

step3:
manage.py syncdb

step4:
open the database "TriAquae", add groups' name into "hosts_group". You can use batach_add_server.py to add a lots of hosts into mysql.
run backend/muti_ping3.py it will put the results of ping into "hosts_serverstatus" automatically

step5:
run backend/collect_hardware_information.py and write_mysql.py, it will put the assets' information into "hosts_devinfo"

step6:
manage.py runserver ip:port
http://ip:port/assets_management
http://ip:port/server_status
http://ip:port/command_execution
http;//ip:port/file_transfer




