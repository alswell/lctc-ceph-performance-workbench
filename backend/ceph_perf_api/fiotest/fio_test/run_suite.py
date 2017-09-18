import os
import sys
import argparse
import datetime
import shutil
import subprocess
import re
import time
import platform
import paramiko
import json
import yaml

from result import Result
from collect_system_info import SysInfo


class RunFIO(SysInfo):
    def __init__(self, test_path, clusterid):
        super(RunFIO, self).__init__(test_path, clusterid)
        self.result = Result(test_path, clusterid)

    def install_deps(self):
        dep_p = {'sysstat': '/usr/bin/sar', 'smartmontools': '/usr/sbin/smartctl'}
        for host in self.host_list:
            ip = self.nodes[host]['ip']
            password = self.nodes[host]['password']
            for p, exe in dep_p.items():
                cmd = "sshpass -p {} ssh {} 'if [ ! -f {} ]; then yum install -y {}; fi'".format(password, ip, exe, p)
                subprocess.check_call(cmd, shell=True)

    def checkandstart_fioser_allclient(self):
        for client, client_info in self.clients.items():
            client = client_info['ip']
            password = client_info['password']
            self.checkandstart_fioser(client, password=password)

    def create_log_dir(self, jobname, jobtime):
        jobtime = re.sub('-', '_', jobtime)
        jobtime = re.sub(':', '_', jobtime)
        jobtime = re.sub(' ', '_', jobtime)

        log_dir = '{}/{}_{}'.format(
            self.test_path,
            jobname,
            jobtime
        )
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def get_ceph_default_value(self, ceph_key):
        result, columns = self.deploydb.query_config(self.clusterid)
        for column in columns:
            if column[0] == 'total':
                total_index = columns.index(column)
                break
        
        default_configs = json.loads(result[-1][total_index])
        return default_configs[ceph_key]

    def set_default_ceph_config(self, ceph_config):
        default_config = {}
        for ceph_key, ceph_value in ceph_config.items():
            default_value = self.get_ceph_default_value(ceph_key)
            default_config[ceph_key] = default_value

        restart = self.modify_ceph_config(default_config)
        if restart:
            print datetime.datetime.now(),
            print "restart ceph for config changed."
            self.reset_ceph_conffile()
            self.restart_ceph()
 

    def check_job_status(self, jobid, ceph_config={}):
        if self.havedb:
            db = self.FioDB()
            job_status = db.query_jobs(jobid)[0][3]
            if (job_status == "Canceling" or job_status == "Canceled"):
                job_info = {'status': "Canceled"}
                db.update_jobs(jobid, **job_info)
                self.set_default_ceph_config(ceph_config)
                raise Exception("Job Canceled!!!")

    def run(self, jobname, jobid, ceph_config={}, sysdata=[]):
        self.check_job_status(jobid)
        if self.havedb:
            self.check_job_status(jobid)
            job_info = {'status': "Install dependence packages"}
            self.fiodb.update_jobs(jobid, **job_info)
        self.install_deps()
        jobname = re.sub('_', '', jobname)
        casenum = len(self.search('{}/config/'.format(self.test_path), '_0.config'))
        jobtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        cephconfig = ''
        for key, value in ceph_config.items():
            value = re.sub('\/', '', str(value))
            key = re.sub('_', '', key)
            cephconfig = cephconfig + key + value + '_'
        if cephconfig == '':
            cephconfig = 'default_'
        print datetime.datetime.now(),
        print "modify_ceph_config"
        if self.havedb:
            self.check_job_status(jobid, ceph_config=ceph_config)
            job_info = {'status': "Modify ceph config"}
            self.fiodb.update_jobs(jobid, **job_info)
        restart = self.modify_ceph_config(ceph_config)
        if restart:
            print datetime.datetime.now(),
            print "restart ceph for config changed."
            self.update_ceph_conffile(ceph_config)
            self.restart_ceph()


        log_dir = self.create_log_dir(jobname, jobtime)

        if self.havedb:
            self.check_job_status(jobid, ceph_config=ceph_config)
            job_info = {'status': "Collecting sys info"}
            self.fiodb.update_jobs(jobid, **job_info)

        print datetime.datetime.now(),
        print "sysinfo.get_all_host_sysinfo_logfile"
        self.get_all_host_sysinfo_logfile('{}/sysinfo'.format(log_dir))
        print datetime.datetime.now(),
        print "sysinfo.deal_with_sysinfo_logfile"
        self.deal_with_sysinfo_logfile(
            '{}/sysinfo'.format(log_dir),
            jobid,
            sysdata,
        )

        configs = os.listdir('{}/config/'.format(self.test_path))
        if self.havedb:
            self.check_job_status(jobid, ceph_config=ceph_config)
            jobinfo = {
                'status': 'Running',
                'casenum': casenum,
                'starttime': jobtime,
            }
            self.fiodb.update_jobs(jobid, **jobinfo)

        with open('{}/fioserver_list.conf'.format(self.test_path), 'r') as f:
            clients = f.readlines()
            num_clients = len(clients)
            i = 0
            while (i < len(configs)):
                if self.havedb:
                    self.check_job_status(jobid, ceph_config=ceph_config)
                match_config = re.match(r'(.*)_0\.config', configs[i])
                if match_config:
                    cmd = ['fio']
                    n = 0
                    for client in clients:
                        config = '{}_{}.config'.format(match_config.group(1), n)
                        if configs.count(config) == 0:
                            raise Exception("can't find {} in {}/config/!".format(config, self.test_path), config)
                        cmd = cmd + ['--client', client.strip(), '{}/config/{}'.format(self.test_path, config)]
                        n = n + 1
                    i = i + 1
                    log_file_name = '{}_{}'.format(
                        match_config.group(1),
                        time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
                    )
                    log_file = '{}/{}.txt'.format(
                        log_dir,
                        log_file_name
                    )

                    fio_runtime = subprocess.check_output(
                        'grep runtime= {}/config/{}_0.config'.format(self.test_path, match_config.group(1)),
                        shell=True)
                    match_runtime = re.match('runtime=(\d+)\D', fio_runtime)
                    timeout = int(match_runtime.group(1)) * 3
                    time_start = time.time()
                    time_out_status = False

                    print datetime.datetime.now(),
                    print "cleanup_ceph_perf"
                    self.cleanup_ceph_perf()
                    print datetime.datetime.now(),
                    print cmd
                    child = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
                    print datetime.datetime.now(),
                    print "get_sys_data"
                    self.get_sys_data()
                    with open(log_file, 'wt') as handle:
                        while True:
                            if time.time() - time_start > timeout:
                                time_out_status = True
                                child.kill()
                                break
                            line = child.stdout.readline()
                            if not line:
                                break
                            print line
                            sys.stdout.flush()
                            handle.write(line)
                        time.sleep(1)
                        if time_out_status:
                            handle.write('\nTimeout')
                            print "Error: Run fio test {} time out in {} s!".format(log_dir, timeout)
                        else:
                            handle.write('\nPass')
                    print datetime.datetime.now(),
                    print "result.deal_with_fio_data"
                    case_status = self.result.deal_with_fio_data(log_dir, log_file_name, jobid)
                    if case_status == "Pass":
                        print datetime.datetime.now(),
                        print "sysdata.get_all_host_sysdata_logfile"
                        self.get_all_host_sysdata_logfile('{}/sysdata_{}'.format(log_dir, log_file_name))
                        time.sleep(1)
                        print datetime.datetime.now(),
                        print "sysdata.deal_with_sysdata_logfile"
                        self.deal_with_sysdata_logfile(
                            log_dir,
                            'sysdata_{}'.format(log_file_name),
                            sysdata,
                        )
                else:
                    i = i + 1
        print datetime.datetime.now(),
        print "set_default_ceph_config"
        self.set_default_ceph_config(ceph_config)
        print datetime.datetime.now(),
        print "gen_result"
        self.gen_result(log_dir)
    
        if self.havedb:
            job_info = {'status': "Finished"}
            self.fiodb.update_jobs(jobid, **job_info)
        return log_dir

    def gen_result(self, log_dir):
        print log_dir
        log_dir_list = log_dir.split('/')
        jobtag = log_dir_list[-1]
        output_file = self.result.deal_with_fio_data_toexcel(
            './result_{}'.format(jobtag),
            log_dir
        )
        print "============================="
        print output_file
        print "============================="

    def reset_ceph_conffile(self):
        org_file = '{}/../../{}_ceph.conf'.format(self.test_path, self.clusterid)
        for node in self.host_list:
            host = self.nodes[node]['ip']
            t = paramiko.Transport(host, "22")
            t.connect(username = "root", password = self.nodes[node]['password'])
            sftp = paramiko.SFTPClient.from_transport(t)
            remotepath = '/etc/ceph/ceph.conf'
            print org_file, remotepath
            sftp.put(org_file, remotepath)
            t.close()

    def update_ceph_conffile(self, ceph_config):
        for node in self.host_list:
            host = self.nodes[node]['ip']
            t = paramiko.Transport(host, "22")
            t.connect(username = "root", password = self.nodes[node]['password'])
            sftp = paramiko.SFTPClient.from_transport(t)
            remotepath = '/etc/ceph/ceph.conf'
            with open('/tmp/ceph.conf', 'w') as output_f:
                file_name = '{}_ceph.conf'.format(self.clusterid)
                with open('{}/../../{}'.format(self.test_path, file_name), 'r') as input_f:
                    for line in input_f.readlines():
                        if re.match('\[osd\]', line):
                            output_f.write(line)
                            for ceph_key, ceph_value in ceph_config.items():
                                output_f.write('{} = {}\n'.format(ceph_key, ceph_value))
                        else:
                            output_f.write(line)
                
            sftp.put('/tmp/ceph.conf', remotepath)
            t.close()

    def restart_ceph(self):
        for node in self.host_list:
            host = self.nodes[node]['ip']
            password = self.nodes[node]['password']
            cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} \
                'service ceph-osd.target restart'".format(password, host)
            subprocess.check_call(cmd, shell=True)
        while True:
            time.sleep(5)
            cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} \
                'ceph health'".format(self.client_password, self.client)
            output = subprocess.check_output(cmd, shell=True)
            print output
            if re.match('HEALTH_OK', output):
                break


    def modify_ceph_config(self, ceph_config):
        print ceph_config
        restart = False
        for ceph_key, ceph_value in ceph_config.items():
            if ceph_value == "false" or ceph_value == "true":
                cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'ceph tell osd.* injectargs --{}={} 2>&1'".format(
                    self.client_password,
                    self.client,
                    ceph_key,
                    ceph_value
                )
            else:
                cmd = "sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'ceph tell osd.* injectargs --{} {} 2>&1'".format(
                    self.client_password,
                    self.client,
                    ceph_key,
                    ceph_value
                )
            print cmd
            output = subprocess.check_output(cmd, shell=True)
            if re.search('\(not observed, change may require restart\)', output):
                restart = True

        return restart

    def _modify_ceph_config(self, ceph_config):
        print ceph_config
        org_all_config = {}
        for host in self.host_list:
            org_host_config = {}
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
            ssh.connect(
                hostname = self.nodes[host]['ip'],
                port = 22,
                username = 'root',
                password = self.host_password
            )
            cmd = 'find /var/run/ceph -name \'*osd*asok\''
            stdin, stdout, stderr = ssh.exec_command(cmd)
            osd_list = stdout.readlines()
            for osd in osd_list:
                org_osd_config = {}
                osd = osd.strip()
                for ceph_key, ceph_value in ceph_config.items():
                    cmd = 'ceph --admin-daemon {} config show | grep -w {}'.format(osd, ceph_key)
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    output = stdout.readlines()
                    if len(output) < 1:
                        raise Exception("Error: Can't find {} in ceph conf!".format(ceph_key), ceph_key)
                    elif len(output) > 1:
                        raise Exception("Error: find {} in ceph conf fail:{}".format(ceph_key, output), ceph_key)
                    else:
                        cephkey_match = re.search('".*": "(.*)",', output[0])
                        org_osd_config[ceph_key] = cephkey_match.group(1)
                    cmd = 'ceph --admin-daemon {} config set {} "{}"'.format(osd, ceph_key, ceph_value)
                    print cmd
                    ssh.exec_command(cmd)
                org_host_config[osd] = org_osd_config
            org_all_config[host] = org_host_config
            ssh.close()
            timetag = update_ceph_conffile(self.nodes[host]['ip'], ceph_config)
        return org_all_config, timetag
 
    def reset_ceph_config(self, org_all_config, timetag):
        for host, host_config in org_all_config.items():
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
            ssh.connect(
                hostname = self.nodes[host]['ip'],
                port = 22,
                username = 'root',
                password = self.host_password
            )
            for osd, osd_config in host_config.items():
                for cephkey, value in osd_config.items():
                    value = re.sub(r'\\', '', value)
                    cmd = 'ceph --admin-daemon {} config set {} "{}"'.format(osd, cephkey, value)
                    print cmd
                    ssh.exec_command(cmd)
            cmd = "cp /etc/ceph/ceph.conf.org.{} /etc/ceph/ceph.conf".format(timetag)
            ssh.exec_command(cmd)
            cmd = "service ceph-osd.target restart"
            ssh.exec_command(cmd)
            ssh.close()
            

    def store_logfile_FS(self, log_dir):
        if log_dir[-1] == '/':
            del log_dir[-1]
        dir_name = log_dir.split('/')[-2]

        FShost = "10.240.217.74"
        cmd = ['sshpass', '-p', 'passw0rd', 'scp', '-o', 'StrictHostKeyChecking=no', '-r', '{}/../../{}'.format(log_dir, dir_name), 'root@{}:/usr/share/fiotest/'.format(FShost)]
        print cmd
        subprocess.check_call(cmd)

    def search(self, path, word):
        output = []
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isfile(fp) and word in filename:
                output.append(fp)
            elif os.path.isdir(fp):
                search(fp, word)
        return output
