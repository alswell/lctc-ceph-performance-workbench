import os
import sys
import argparse
import datetime
import shutil
import subprocess
import re
import time
import paramiko
from multiprocessing import Process
import json
import yaml
import socket,struct


class SysInfo(object):

    def __init__(self, client, havedb=False):
        if havedb:
            from todb import ToDB
            self.db = ToDB()
        self.havedb = havedb
        self.intervaltime = 1
        self.ceph_intervaltime = 10
        self.monnum = 0

        self.hwinfo_file = '{}/../../ceph_hw_info.yml'.format(os.getcwd())
        with open(self.hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)
        self.nodes = ceph_info['ceph-node']
        self.network = ceph_info['ceph-network']
        #self.nodes = get_ceph_config_file('/tmp/', client)['ceph-node']

        self.client_password = False
        if ceph_info['ceph-client'].has_key(client):
            self.client = ceph_info['ceph-client'][client]['ip']
            self.client_password = ceph_info['ceph-client'][client]['password']
        else:
            for client_name, client_data in ceph_info['ceph-client'].items():
                if client == client_data['ip']:
                    self.client = client_data['ip']
                    self.client_password = client_data['password']
        if not self.client_password:
            print "Error: can't find {} in ceph_hw_info.yml.".format(client)
            sys.exit(1)

        self.client_password = str(self.client_password)
        self.host_password = "passw0rd"

        self.host_list = []
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.client, port=22, username='root', password=self.client_password)
        cmd = 'ceph osd tree | grep host'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.readlines()
        for item in output:
            match = re.search('host (\S*)\s+', item)
            self.host_list.append(match.group(1))

    def run_sshcmds(self, host, cmds, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = password
        )
        for cmd in cmds:
            print "exec {} in {}.".format(cmd, host)
            ssh.exec_command(cmd)
        ssh.close()

    def sys_info(self, host):
        cmds = [
            'sar -A {} >/tmp/sar.txt &'.format(self.intervaltime),
            'date >/tmp/iostat.txt; iostat -p -dxm {} >>/tmp/iostat.txt &'.format(self.intervaltime),
        ]
        self.run_sshcmds(host, cmds, self.host_password)

    def get_sys_info(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            print 'get sysinfo {}'.format(host)
            p = Process(target=self.sys_info, args=(host_ip,))
            p.start()
        self.get_ceph_status(self.client)

    def get_ceph_status(self, client):
        cmds = [
            'date >/tmp/cephstatus.txt; while true; do ceph -s --format json-pretty; sleep {}; done >>/tmp/cephstatus.txt &'.format(self.ceph_intervaltime),
            'ceph -v >/tmp/cephv.txt',
            'ceph df -f json-pretty >/tmp/cephdf.json',
            'ceph osd tree -f json-pretty >/tmp/cephosdtree.json',
        ]
        self.run_sshcmds(client, cmds, self.client_password)

    def cleanup_sys_info(self, host):
        cmds = [
            'kill -9 `ps -ef | grep sar | grep -v grep | awk \'{print $2}\'`',
            'kill -9 `ps -ef | grep iostat | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(host, cmds, self.host_password)

    def cleanup_all(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            print 'cleanup sysinfo collect process in {}'.format(host)
            p = Process(target=self.cleanup_sys_info,args=(host_ip,))
            p.start()
        cmd = [
            'kill -9 `ps -ef | grep \'ceph -s\' | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(self.client, cmd, self.client_password)


    def get_logfile(self, host, password, log, log_dir):
        t = paramiko.Transport(host, "22")
        t.connect(username = "root", password = password)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath = '/tmp/{}'.format(log)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception, e:
                print "make sysinfo log dir fail:{}".format(e)
                sys.exit(1)

        localpath = '{}/{}_{}'.format(log_dir, host, log)
        print host, remotepath, localpath
        sftp.get(remotepath, localpath)
        t.close()

    def get_all_logfile(self, host, log_dir):
        self.get_hwinfo_log(host, log_dir)
        self.get_logfile(host, self.host_password, 'sar.txt', log_dir)
        self.get_logfile(host, self.host_password, 'iostat.txt', log_dir)
        self.get_logfile(host, self.host_password, 'dmidecode.txt', log_dir)
        self.get_logfile(host, self.host_password, 'meminfo.txt', log_dir)
        self.get_logfile(host, self.host_password, 'cpuinfo.txt', log_dir)
        self.get_logfile(host, self.host_password, 'lsblk.txt', log_dir)

    def get_all_host_logfile(self, log_dir):
        self.cleanup_all()
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            self.get_all_logfile(host_ip, log_dir)
            self.get_ceph_perfdump(host_ip, log_dir)
            self.get_ceph_conf(host_ip, log_dir)

        self.get_logfile(self.client, self.client_password, 'cephstatus.txt', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephv.txt', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephdf.json', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephosdtree.json', log_dir)

    def get_hwinfo_log(self, host_ip, log_dir):
        cmds = [
            'dmidecode >/tmp/dmidecode.txt',
            'cat /proc/meminfo >/tmp/meminfo.txt',
            'cat /proc/cpuinfo >/tmp/cpuinfo.txt',
            'lsblk >/tmp/lsblk.txt',
        ]
        self.run_sshcmds(host_ip, cmds, self.host_password)

    def get_ceph_perfdump(self, host, log_dir):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = self.host_password
        )
        cmd = 'find /var/run/ceph -name \'*osd*asok\''
        stdin, stdout, stderr = ssh.exec_command(cmd)
        osd_list = stdout.readlines()
        ceph_perfdump_file_list = []
        for osd in osd_list:
            osd = osd.strip()
            cmd = 'ceph --admin-daemon {} perf dump > /tmp/{}_ceph_perfdump.json'.format(
                osd,
                re.search('(osd\.\d+)', osd).group(1)
            )
            ssh.exec_command(cmd)
            ceph_perfdump_file_list.append('{}_ceph_perfdump.json'.format(
                re.search('(osd\.\d+)', osd).group(1)
            ))
        ssh.close()

        t = paramiko.Transport(host, "22")
        t.connect(username = "root", password = self.host_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception, e:
                print "make sysinfo log dir fail:{}".format(e)
                sys.exit(1)
        for log in ceph_perfdump_file_list:
            remotepath = '/tmp/{}'.format(log)
            localpath = '{}/{}_{}'.format(log_dir, host, log)
            print host, remotepath, localpath
            sftp.get(remotepath, localpath)
        t.close()

    def cleanup_ceph_perf(self):
        for host in self.host_list:
            cmds = ['find /var/run/ceph -name \'*osd*asok\' | while read path; do ceph --admin-daemon $path perf reset all; done']
            self.run_sshcmds(self.nodes[host]['public_ip'], cmds, self.host_password)

    def get_ceph_conf(self, host, log_dir):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = self.host_password
        )
        cmd = 'find /var/run/ceph -name \'*osd*asok\''
        stdin, stdout, stderr = ssh.exec_command(cmd)
        osd_list = stdout.readlines()
        ceph_config_file_list = []
        for osd in osd_list:
            osd = osd.strip()
            cmd = 'ceph --admin-daemon {} config show > /tmp/{}_ceph_config.json'.format(
                osd,
                re.search('(osd\.\d+)', osd).group(1)
            )
            ssh.exec_command(cmd)
            ceph_config_file_list.append('{}_ceph_config.json'.format(
                re.search('(osd\.\d+)', osd).group(1)
            ))
        ssh.close()

        t = paramiko.Transport(host, "22")
        t.connect(username = "root", password = self.host_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception, e:
                print "make sysinfo log dir fail:{}".format(e)
                sys.exit(1)
        for log in ceph_config_file_list:
            remotepath = '/tmp/{}'.format(log)
            localpath = '{}/{}_{}'.format(log_dir, host, log)
            print host, remotepath, localpath
            sftp.get(remotepath, localpath)
        t.close()

    def get_datetime_fordb_sarlog(self, time, t_type, casename):
        if t_type == 'PM':
            time_list = time.split(':')
            hour = time_list[0]
            if int(hour) == 12:
                hour = 0
            _time = '{}:{}:{}'.format(
                int(hour) + 12,
                time_list[1],
                time_list[2]
            )
        else:
            _time = time

        casename_list = casename.split('_')  #rbd_rw_4k_runtime30_iodepth1_numjob1_imagenum2_test2_%70_2017_07_27_17_47_33
        result_time = '{}-{}-{} {}'.format(
            casename_list[-6],
            casename_list[-5],
            casename_list[-4],
            _time
        )
        return result_time

    def deal_with_sarlog_cpu(self, host, casename):
        #%usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
        cpu_result = []
        cmd = 'grep "CPU      %usr" -A 1 {}_sar.txt | grep all'.format(self.nodes[host]['public_ip'])
        cpu_data_list = subprocess.check_output(cmd, shell=True).split('\n')
        del cpu_data_list[-1]
        for cpu_data in cpu_data_list:
            result = {}
            cpu_data = re.sub(r'\s+', ",", cpu_data)
            cpu_data = cpu_data.split(',')
            result['time'] = self.get_datetime_fordb_sarlog(cpu_data[0], cpu_data[1], casename)
            result['usr'] = cpu_data[3]
            result['nice'] = cpu_data[4]
            result['sys'] = cpu_data[5]
            result['iowait'] = cpu_data[6]
            result['steal'] = cpu_data[7]
            result['irq'] = cpu_data[8]
            result['soft'] = cpu_data[9]
            result['guest'] = cpu_data[10]
            result['gnice'] = cpu_data[11]
            result['idle'] = cpu_data[12]
            cpu_result.append(result)
            if self.havedb:
                self.db.insert_tb_sarcpudata(casename, host, **result)
        return cpu_result

    def deal_with_sarlog_memory(self, host, casename):
        #kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
        mem_result = []
        with open('{}_sar.txt'.format(self.nodes[host]['public_ip']), 'r') as f:
            lines = f.readlines()
            mem_data_list = []
            for n in range(len(lines)):
                if re.search('kbmemfree kbmemused', lines[n]):
                    mem_data_list.append(lines[n+1].strip())
        for mem_data in mem_data_list:
            result = {}
            mem_data = re.sub(r'\s+', ",", mem_data)
            data = mem_data.split(',')
            result['time'] = self.get_datetime_fordb_sarlog(data[0], data[1], casename)
            result['kbmemfree'] = data[2]
            result['kbmemused'] = data[3]
            result['memused'] = data[4]
            result['kbbuffers'] = data[5]
            result['kbcached'] = data[6]
            result['kbcommit'] = data[7]
            result['commit'] = data[8]
            result['kbactive'] = data[9]
            result['kbinact'] = data[10]
            result['kbdirty'] = data[11]
            mem_result.append(result)
            if self.havedb:
                self.db.insert_tb_sarmemdata(casename, host, **result)
        return mem_result

    def get_network_device(self, host):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=self.nodes[host]['public_ip'], port=22, username='root', password=self.host_password)
        stdin, stdout, stderr = ssh.exec_command(
            'ifconfig | grep "inet " -B 1')
        result = stdout.read()
        ssh.close()

        results = result.split('--')
        for result in results:
            result = re.sub('\n', '', result)
            match = re.match('(\S+):.*inet (\S+) ', result)
            ip = match.group(2)
            if self.nodes[host]['public_ip'] == ip:
                public_n = match.group(1)
            elif ip_in_subnet(ip, self.network['cluster_network']):
                cluster_n = match.group(1)

        return cluster_n, public_n

    def deal_with_sarlog_nic(self, host, casename):
        #rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
        cluster_n, public_n = self.get_network_device(host)
        with open('{}_sar.txt'.format(self.nodes[host]['public_ip']), 'r') as f:
            lines = f.readlines()
            nic_data_list = []
            for n in range(len(lines)):
                if re.search(r'rxpck\/s   txpck\/s', lines[n]):
                    i = 1
                    while lines[n+i] != '\n':
                        nic_data_list.append(lines[n+i].strip())
                        i = i+1
        both_result = {}
        cluster_result = []
        public_result = []
        for nic_data in nic_data_list:
            result = {}
            nic_data = re.sub(r'\s+', ",", nic_data)
            data = nic_data.split(',')
            if data[2] == cluster_n:
                result['time'] = self.get_datetime_fordb_sarlog(data[0], data[1], casename)
                result['rxpcks'] = data[3]
                result['txpcks'] = data[4]
                result['rxkBs'] = data[5]
                result['txkBs'] = data[6]
                result['rxcmps'] = data[7]
                result['txcmps'] = data[8]
                result['rxmcsts'] = data[9]
                cluster_result.append(result)
                if self.havedb:
                    self.db.insert_tb_sarnicdata(
                        casename,
                        host,
                        'cluster:{}'.format(cluster_n),
                        **result
                    )
            elif data[2] == public_n:
                result['time'] = self.get_datetime_fordb_sarlog(data[0], data[1], casename)
                result['rxpcks'] = data[3]
                result['txpcks'] = data[4]
                result['rxkBs'] = data[5]
                result['txkBs'] = data[6]
                result['rxcmps'] = data[7]
                result['txcmps'] = data[8]
                result['rxmcsts'] = data[9]
                public_result.append(result)
                if self.havedb:
                    self.db.insert_tb_sarnicdata(
                        casename,
                        host,
                        'public:{}'.format(public_n),
                        **result
                    )
        both_result['cluster_network:{}'.format(cluster_n)] = cluster_result
        both_result['public_network:{}'.format(public_n)] = public_result

        return both_result

    def deal_with_sarlog(self, casename):
        all_result = {}
        for host in self.host_list:
            all_result[host] = self.deal_with_sarlog_cpu(host, casename)
        json.dump(all_result, open('./sar_cpu.json', 'w'), indent=2)

        for host in self.host_list:
            all_result[host] = self.deal_with_sarlog_memory(host, casename)
        json.dump(all_result, open('./sar_memory.json', 'w'), indent=2)

        for host in self.host_list:
            all_result[host] = self.deal_with_sarlog_nic(host, casename)
        json.dump(all_result, open('./sar_nic.json', 'w'), indent=2)

    def get_datetime_fordb_iostatlog(self, casename, time, n):
        time_match = re.match('(.*):(.*):(.*)', time)
        sec = int(time_match.group(3)) + n
        if sec > 59:
            minu = int(time_match.group(2)) + 1
            if minu == 60:
                hour = int(time_match.group(1)) + 1
                if hour == 24:
                    _time = '00:00:{:0>2}'.format(sec%60)
                else:
                    _time = '{}:00:{:0>2}'.format(hour, sec%60)
            else:
                _time = '{}:{}:{:0>2}'.format(time_match.group(1), minu, sec%60)
        else:
            _time = _time = '{}:{}:{:0>2}'.format(time_match.group(1), time_match.group(2), sec)

        casename_list = casename.split('_')

        result_time = '{}-{}-{} {}'.format(
            casename_list[-6],
            casename_list[-5],
            casename_list[-4],
            _time
        )
        return result_time

    def deal_with_iostatlog(self, casename):
        #rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util

        all_result = {}
        for host in self.host_list:
            osd_result = {}

            with open('{}_iostat.txt'.format(self.nodes[host]['public_ip'])) as f:
                time = f.readline()
            osd_result['start_time'] = re.search(' (\S*:.*:\S*) ', time).group(1)

            for osd_num,osd in self.nodes[host]['osd'].items():
                oj_result = {}
                for disk_name,disk in osd.items():
                    osd_disk = disk.split('/')[-1]
                    #osd_disk = re.match('/dev/(.*)', disk).group(1)
                    disk_result = []
                    cmd = 'grep "{}" {}_iostat.txt'.format(osd_disk, self.nodes[host]['public_ip'])
                    disk_data_list = subprocess.check_output(cmd, shell=True).split('\n')
                    del disk_data_list[0]
                    del disk_data_list[-1]
                    n = 0
                    for disk_data in disk_data_list:
                        result = {}
                        disk_data = re.sub(r'\s+', ",", disk_data)
                        data = disk_data.split(',')
                        result['time'] = self.get_datetime_fordb_iostatlog(casename, osd_result['start_time'], n)
                        result['rrqms'] = data[1]
                        result['wrqms'] = data[2]
                        result['rs'] = data[3]
                        result['ws'] = data[4]
                        result['tps'] = float(data[3])+float(data[4])
                        result['rMBs'] = data[5]
                        result['wMBs'] = data[6]
                        result['avgrqsz'] = data[7]
                        result['avgqusz'] = data[8]
                        result['await'] = data[9]
                        result['r_await'] = data[10]
                        result['w_await'] = data[10]
                        result['svctm'] = data[10]
                        result['util'] = data[10]
                        disk_result.append(result)
                        if self.havedb:
                            self.db.insert_tb_iostatdata(casename, host, osd_num, disk_name+':'+disk, **result)
                        n = n + self.intervaltime
                    oj_result[disk_name] = disk_result
                osd_result[osd_num] = oj_result
            all_result[host] = osd_result
        json.dump(all_result, open('./iostat.json', 'w'), indent=2)

    def deal_with_perfdumplog(self, casename):
        log_files = os.popen('ls *ceph_perfdump.json').readlines()
        for log_file in log_files:
            log_file = log_file.strip()
            host = log_file.split('_')[0]
            log_osd = log_file.split('_')[1]
            perfdump = json.load(open(log_file))
            self.db.insert_tb_perfdumpdata(casename, host, log_osd, **perfdump)

    def deal_with_cephconfiglog(self, casename):
        log_files = os.popen('ls *ceph_config.json').readlines()
        for log_file in log_files:
            log_file = log_file.strip()
            host = log_file.split('_')[0]
            osd = log_file.split('_')[1]
            ceph_configs = json.load(open(log_file))
            self.db.insert_tb_cephconfigdata(casename, host, osd, **ceph_configs)

    def deal_with_cephstatuslog(self, casename):
        log_file = '{}_cephstatus.txt'.format(self.client)
        with open(log_file, 'r') as f:
            json_start = False
            rawtime = f.readline()
            rawtime = re.search(' (\S*:.*:\S*) ', rawtime).group(1)
            n = 0
            for line in f.readlines():
                time = self.get_datetime_fordb_iostatlog(casename, rawtime, n)
                n = n+self.ceph_intervaltime
                if re.match('{', line):
                    json_start = True
                    line_to_file = []
                if json_start:
                    line_to_file.append(line)
                if re.match('}', line):
                    json_start = False
                    with open('/tmp/ceph_tmp.txt', 'w') as output_f:
                        for output_line in line_to_file:
                            output_f.write(output_line)
                    ceph_status = json.load(open('/tmp/ceph_tmp.txt'))
                    self.monnum = len(ceph_status['monmap']['mons'])
                    ceph_mon = str(ceph_status['monmap']['mons'])
                    ceph_map = str(ceph_status['pgmap']['pgs_by_state'])
                    ceph_mon = re.sub('\'', '\\\'', ceph_mon)
                    ceph_map = re.sub('\'', '\\\'', ceph_map)
                    ceph_status['monmap']['mons'] = ceph_mon
                    ceph_status['pgmap']['pgs_by_state'] = ceph_map
                    self.db.insert_tb_cephstatusdata(casename, time, **ceph_status)

    def deal_with_smartctl(self, result):
        model = ''
        speed = ''
        for line in result:
            model_match = re.match('Device Model:\s+(.*)$', line)
            speed_match = re.match('Rotation Rate::\s+(.*)$', line)
            if model_match:
                model = model_match.group(1)
            if speed_match:
                speed = speed_match.group(1)
        return model, speed

    def deal_with_lsblk_log(self, casename):
        disk_info = {}
        for host in self.host_list:
            ip = self.nodes[host]['public_ip']
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname = ip,
                port = 22,
                username = 'root',
                password = self.host_password
            )
 
            with open('{}_lsblk.txt'.format(ip), 'r') as f:
                f.readline()
                for line in f.readlines():
                    match = re.match('(\w+)\s+\S+\s+\S+\s+(\S+)', line)
                    if match:
                        disk_name = match.group(1)
                        disk_size = match.group(2)
                        cmd = 'smartctl -i /dev/{}'.format(disk_name)
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        result = stdout.read()
                        with open('{}_{}_smartctl.txt'.format(ip, disk_name), 'w') as smartctl_f:
                            smartctl_f.write(result)
                        disk_model, disk_speed = self.deal_with_smartctl(result)
                        if self.havedb:
                            self.db.insert_tb_diskinfo(
                                casename,
                                host,
                                disk_name,
                                disk_size,
                                disk_model,
                                disk_speed
                            )
            ssh.close()


    def deal_with_cpuinfo_log(self):
        cpu_info = {}
        for host in self.host_list:
            with open('{}_cpuinfo.txt'.format(self.nodes[host]['public_ip']), 'r') as f:
                cpunum = 0
                cputype = ''
                cpuspeed = ''
                cpucores = ''
                for line in f:
                    match_cputype = re.match('model name\s+: (.*)$', line)
                    match_cpuspeed = re.match('cpu MHz\s+: (.*)$', line)
                    match_cpucores = re.match('cpu cores\s+: (.*)$', line)
                    if match_cputype:
                        cputype = match_cputype.group(1)
                        cpunum = cpunum + 1
                    if match_cpuspeed:
                        cpuspeed = match_cpuspeed.group(1)
                    if match_cpucores:
                        cpucores = match_cpucores.group(1)
            cpu_info[host] = {
                'cputype': cputype,
                'cpuspeed': cpuspeed,
                'percpucores': cpucores,
                'cpunum': cpunum
            }
        return cpu_info 

    def deal_with_meminfo_log(self):
        mem_info = {}
        for host in self.host_list:
            with open('{}_dmidecode.txt'.format(self.nodes[host]['public_ip']), 'r') as f:
                n = 0
                memnum = 0
                mem_match = False
                mem_M = ''
                mem_S = ''
                lines = f.readlines()
                while n < len(lines):
                    if re.match('Memory Device$', lines[n]):
                        memnum = memnum + 1
                        mem_match = True
                    if mem_match:
                        M_match = re.match('\s*Manufacturer: (.*)$', lines[n])
                        S_match = re.match('\s*Serial Number: (.*)$', lines[n])
                        if M_match:
                            mem_M = M_match.group(1)
                        if S_match:
                            mem_S = S_match.group(1)
                        if re.match('$', lines[n]):
                            mem_match = False
                    n = n+1
            with open('{}_meminfo.txt'.format(self.nodes[host]['public_ip']), 'r') as f:
                for line in f:
                    maxsize_match = re.match('MemTotal:\s+(.*)$', line)
                    if maxsize_match:
                        memsize = maxsize_match.group(1)
            mem_info[host] = {'memtype': mem_M+':'+mem_S, 'totalsize': memsize, 'memnum': memnum}
        return mem_info 

    def deal_with_hwinfo(self, casename):
        cpu_info = self.deal_with_cpuinfo_log()
        mem_info = self.deal_with_meminfo_log()
        for host in self.host_list:
            hw_info = {}
            hw_info.update(cpu_info[host])
            hw_info.update(mem_info[host])
            hw_info.update(self.nodes[host]['hwinfo'])
            json.dump(hw_info, open('./{}_hw_info.json'.format(host), 'w'), indent=2)
            if self.havedb:
                self.db.insert_tb_hwinfo(casename, host, **hw_info)

    def get_pool_info(self, pools):
        pool_info = {}
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = self.client,
            port = 22,
            username = 'root',
            password = self.client_password
        )
        for pool in pools:
            cmd = 'ceph osd pool get {} size'.format(pool['name'])
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            pool_size = re.match('size: (\d+)', result).group(1)

            cmd = 'ceph osd pool get {} pg_num'.format(pool['name'])
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            pgnum = re.match('pg_num: (\d+)', result).group(1)

            pool_info[pool['name']] = {'size': pool_size, 'pgnum': pgnum }

        return pool_info

    def deal_with_cephinfo(self, casename):
        ceph_info = {'monnum': self.monnum, 'nodenum': len(self.host_list)}

        version_file = '{}_cephv.txt'.format(self.client)
        with open(version_file, 'r') as f:
            ceph_info['version'] = f.readline().strip()

        osdtree_file = '{}_cephosdtree.json'.format(self.client)
        osdtree = json.load(open(osdtree_file))
        osdnum = 0
        for node in osdtree['nodes']:
            if node['type'] == 'osd':
                osdnum = osdnum + 1
        ceph_info['osdnum'] = osdnum
        #ceph_info.update(osdtree)

        df_file = '{}_cephdf.json'.format(self.client)
        df = json.load(open(df_file))
        ceph_info.update(df)

        pools_info = self.get_pool_info(df['pools'])

        ceph_info['pool'] = pools_info
        json.dump(ceph_info, open('./ceph_info.json', 'w'), indent=2)
        if self.havedb:
            self.db.insert_tb_cephinfo(casename, **ceph_info)
            for pool, pool_info in pools_info.items():
                self.db.insert_tb_poolinfo(casename, pool, **pool_info)

    def get_os_info(self, casename):
        for host in self.host_list:
            os_info = {}
            ip = self.nodes[host]['public_ip']
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname = ip,
                port = 22,
                username = 'root',
                password = self.host_password
            )

            cmd = 'cat /proc/sys/vm/dirty_background_ratio'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read()
            os_info['dirty_background_ratio'] = re.sub('\n', '', output)

            cmd = 'cat /proc/sys/vm/dirty_ratio'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read()
            os_info['dirty_ratio'] = re.sub('\n', '', output)

            cmd = 'ps -ef | wc -l'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read()
            os_info['PIDnumber'] = re.sub('\n', '', output)

            os_info.update(self.nodes[host]['osinfo'])

            json.dump(os_info, open('./{}_os_info.json'.format(host), 'w'), indent=2)
            if self.havedb:
                self.db.insert_tb_osinfo(casename, host, **os_info)


    def deal_with_sysinfo_logfile(self, log_dir):
        org_dir = os.getcwd()
        os.chdir(log_dir)
        dir_list = os.getcwd().split('/')
        casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)

        self.deal_with_sarlog(casename)
        self.deal_with_iostatlog(casename)
        if self.havedb:
            self.deal_with_cephconfiglog(casename)
            self.deal_with_perfdumplog(casename)
            self.deal_with_cephstatuslog(casename)
        self.deal_with_lsblk_log(casename)
        self.deal_with_hwinfo(casename)
        self.get_os_info(casename)
        self.deal_with_cephinfo(casename)
        os.chdir(org_dir)

def format_subnet(subnet_input):
    if subnet_input.find("/") == -1:
        return subnet_input + "/255.255.255.255"

    else:
        subnet = subnet_input.split("/")
        if len(subnet[1]) < 3:
            mask_num = int(subnet[1])
            last_mask_num = mask_num % 8
            last_mask_str = ""
            for i in range(last_mask_num):
                last_mask_str += "1"
            if len(last_mask_str) < 8:
                for i in range(8-len(last_mask_str)):
                    last_mask_str += "0"
            last_mask_str = str(int(last_mask_str,2))
            if mask_num / 8 == 0:
                subnet = subnet[0] + "/" + last_mask_str +"0.0.0"
            elif mask_num / 8 == 1:
                subnet = subnet[0] + "/255." + last_mask_str +".0.0"
            elif mask_num / 8 == 2 :
                subnet = subnet[0] + "/255.255." + last_mask_str +".0"
            elif mask_num / 8 == 3:
                subnet = subnet[0] + "/255.255.255." + last_mask_str
            elif mask_num / 8 == 4:
                subnet = subnet[0] + "/255.255.255.255"
            subnet_input = subnet

        subnet_array = subnet_input.split("/")
        subnet_true = socket.inet_ntoa(
            struct.pack(
                "!I",
                struct.unpack(
                    "!I",
                    socket.inet_aton(subnet_array[0])
                )[0] & struct.unpack(
                    "!I",
                    socket.inet_aton(subnet_array[1])
                )[0]
            )
        ) + "/" + subnet_array[1]
        return subnet_true

def ip_in_subnet(ip,subnet):
    subnet = format_subnet(str(subnet))
    subnet_array = subnet.split("/")
    ip = format_subnet(ip + "/" + subnet_array[1])
    return ip == subnet

def get_ceph_config_file_sds(log_dir, client):
    t = paramiko.Transport(client, "22")
    t.connect(username = "root", password = self.client_password)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath = '/etc/ceph/ceph.conf'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception, e:
            print "make log dir fail:{}".format(e)
            sys.exit(1)

    localpath = '{}/{}_ceph.conf'.format(log_dir, client)
    sftp.get(remotepath, localpath)
    t.close()

    output = {}
    nodes = {}
    with open('{}/{}_ceph.conf'.format(log_dir, client), 'r') as f:
        lines = f.readlines()
        n = 0
        while n < len(lines):
            osd_match = re.match('\[(osd\.\d+)\]', lines[n])
            if osd_match:
                host_match = re.match('\s*host = (.*)', lines[n+1])
                publicip_match = re.match('\s*public addr = (\d+.\d+.\d+\.\d+)', lines[n+2])
                clusterip_match = re.match('\s*cluster addr = (\d+.\d+.\d+\.\d+)', lines[n+3])
                osdjournal_match = re.match('\s*osd journal = (.*)', lines[n+5])
                osddata_match = re.match('\s*devs = (.*)', lines[n+4])
                if not osddata_match:
                    osddata_match = re.match('\s*osd data = (.*)', lines[n+6])
                n = n + 6
                host_name = host_match.group(1)
                osd_num = osd_match.group(1)
                if nodes.has_key(host_name):
                    nodes[host_name]['osd'][osd_num] = {
                        'osd-disk': osddata_match.group(1),
                        'journal-disk': osdjournal_match.group(1)
                    }
                else:
                    osd_dic = {}
                    osd_dic[osd_num] = {
                        'osd-disk': osddata_match.group(1),
                        'journal-disk': osdjournal_match.group(1)
                    }
                    nodes[host_name] = {
                        'public_ip': publicip_match.group(1),
                        'cluster_ip': clusterip_match.group(1),
                        'osd': osd_dic}
            else:
                n = n + 1
    output['ceph-node'] = nodes
    return output

def get_ceph_config_file(client):
    osds_num_list = subprocess.check_output('ceph osd ls', shell=True).split('\n')
    del osds_num_list[-1]

    for osd_num in osds_num_list:
        subprocess.check_output('ceph osd find {} >/tmp/osd_tmp.json'.format(osd_num), shell=True)
        output = json.dumps(output)
        print "++++++++++++++++++++++++++"
        print output
        print "++++++++++++++++++++++++++"

def main():
    parser = argparse.ArgumentParser(
        prog="sysinfo",
        version='v0.1',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="collect systen info")
    parser.add_argument('-D', '--logdir', dest="logdir",
                metavar="sysinfo log dir", action="store",
                    help='''sysinfo log dir''')
    args = parser.parse_args()

    client = '10.240.217.101'
    #sysinfo = SysInfo(client)
    '''
    #sysinfo.get_sys_info()
    #sysinfo.cleanup_all()
    sysinfo.deal_with_sysinfo_logfile(
        sysinfo_dir,
    )
    '''
    #sysinfo.deal_with_perfdumplog('/root/fio-zelin/test-suites/test2/log_2017_07_28_15_00_39/sysinfo_rbd_rw_4k_runtime30_iodepth1_numjob1_imagenum2_test2_%70_2017_07_28_15_00_39')
    get_ceph_config_file(client)

if __name__ == '__main__':
    main()
