
import os,sys

Working_dir = '/usr/local/TriAquae3.0'
Web_dir = '/var/www/TriAquae'
Max_batch_threads =  50
Tri_sftp_send_dir = '%s/TriSFTP/send' % Working_dir
Tri_sftp_recv_dir = '%s/TriSFTP/recv' % Working_dir
Dangerous_cmd_list = '%s/share/dangerous_cmd.txt' % Working_dir
RRDTOOL_install_dir = '%s/rrdtool' % Working_dir
RRDTOOL_png_dir = '%s/rrdtool_png' % Web_dir 
RRDTOOL_rrd_file_dir= '%s/rrdtool/rrd_files' % Working_dir

Log_dir = '%s/logs' % Working_dir
Snmp_temp_log = '%s/snmp_temp.log' % Log_dir
Shellinaboxed_install_dir = '%s/shellinaboxed' % Working_dir
Django_install_dir = ''

Tri_connector_username = 'tri_connector'
Tri_connector_password = 'dkeils!3fkd383lsdfksomj=ted_c'

Asset_collection_dir = '%s/asset_collection' % Working_dir

Ops_log_temp_purge_days = 1

SMTP_server = 'smtp.126.com'
Mail_username = 'lijie3721'
Mail_password = 'Motherfucker!23'

Asset_collect_user = 'triaquae'
Asset_user_password = 'efTNmwQtn0TMKIcLtrqr' # needs to be modified automatically

dir_list = [Working_dir, Web_dir, Log_dir,Tri_sftp_send_dir, Tri_sftp_recv_dir, Dangerous_cmd_list, RRDTOOL_install_dir,RRDTOOL_png_dir,RRDTOOL_rrd_file_dir,Shellinaboxed_install_dir,Django_install_dir,Asset_collection_dir]


try:
    if sys.argv[1] == '--initial':
        for d in dir_list:
            try:
                os.mkdir(d)
            except OSError:continue
except IndexError:pass
