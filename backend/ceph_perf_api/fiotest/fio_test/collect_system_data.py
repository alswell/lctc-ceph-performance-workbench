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


class SysData(object):

    def __init__(self, path, client, havedb=False):
        if havedb:
            from todb import ToDB
            self.db = ToDB()
        self.havedb = havedb
        self.intervaltime = 1
        self.ceph_intervaltime = 10
        self.monnum = 0

        self.hwinfo_file = '{}/../../ceph_hw_info.yml'.format(path)
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
            raise Exception("Error: can't find {} in ceph_hw_info.yml.".format(client))

        self.client_password = str(self.client_password)
        node_name, node_data = ceph_info['ceph-node'].popitem()
        self.host_password = node_data['password']
        ceph_info['ceph-node'][node_name] = node_data

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

    def get_logfile(self, host, password, log, log_dir):
        t = paramiko.Transport(host, "22")
        t.connect(username = "root", password = password)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath = '/tmp/{}'.format(log)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        localpath = '{}/{}_{}'.format(log_dir, host, log)
        print host, remotepath, localpath
        sftp.get(remotepath, localpath)
        t.close()


    def sys_data(self, host):
        cmds = [
            'sar -A {} >/tmp/sar.txt &'.format(self.intervaltime),
            'date >/tmp/iostat.txt; iostat -p -dxm {} >>/tmp/iostat.txt &'.format(self.intervaltime),
        ]
        self.run_sshcmds(host, cmds, self.host_password)

    def get_ceph_status(self, client):
        cmds = [
            'date >/tmp/cephstatus.txt; while true; do ceph -s --format json-pretty; sleep {}; done >>/tmp/cephstatus.txt &'.format(self.ceph_intervaltime),
            'ceph -v >/tmp/cephv.txt',
            'ceph df -f json-pretty >/tmp/cephdf.json',
            'ceph osd tree -f json-pretty >/tmp/cephosdtree.json',
        ]
        self.run_sshcmds(client, cmds, self.client_password)

    def get_sys_data(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['ip']
            print 'get sysdata {}'.format(host)
            p = Process(target=self.sys_data, args=(host_ip,))
            p.start()
        self.get_ceph_status(self.client)

    def cleanup_sys_data(self, host):
        cmds = [
            'kill -9 `ps -ef | grep sar | grep -v grep | awk \'{print $2}\'`',
            'kill -9 `ps -ef | grep iostat | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(host, cmds, self.host_password)

    def cleanup_all(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['ip']
            print 'cleanup sysdata collect process in {}'.format(host)
            p = Process(target=self.cleanup_sys_data,args=(host_ip,))
            p.start()
        cmd = [
            'kill -9 `ps -ef | grep \'ceph -s\' | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(self.client, cmd, self.client_password)


    def get_all_logfile(self, host, log_dir):
        self.get_logfile(host, self.host_password, 'sar.txt', log_dir)
        self.get_logfile(host, self.host_password, 'iostat.txt', log_dir)

    def get_all_host_sysdata_logfile(self, log_dir):
        self.cleanup_all()
        for host in self.host_list:
            host_ip = self.nodes[host]['ip']
            self.get_all_logfile(host_ip, log_dir)
            self.get_ceph_perfdump(host_ip, log_dir)

        self.get_logfile(self.client, self.client_password, 'cephstatus.txt', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephv.txt', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephdf.json', log_dir)
        self.get_logfile(self.client, self.client_password, 'cephosdtree.json', log_dir)


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
            print cmd
            ssh.exec_command(cmd)
            ceph_perfdump_file_list.append('{}_ceph_perfdump.json'.format(
                re.search('(osd\.\d+)', osd).group(1)
            ))
        ssh.close()

        time.sleep(1)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        for log in ceph_perfdump_file_list:
            remotepath = '/tmp/{}'.format(log)
            localpath = '{}/{}_{}'.format(log_dir, host, log)
            print host, remotepath, localpath
            cmd = ['sshpass', '-p', self.host_password, 'scp',
                '-o', 'StrictHostKeyChecking=no', '-r',
                'root@{}:{}'.format(host, remotepath), localpath]
            print cmd
            subprocess.check_call(cmd)

    def cleanup_ceph_perf(self):
        for host in self.host_list:
            cmds = [
                'find /var/run/ceph -name \'*osd*asok\' | while read path; do ceph --admin-daemon $path perf reset all; done',
                'lsblk | grep -Eo "ceph-.*" | sed "s/ceph-/osd./g" | while read osd; do ceph daemon $osd flush_store_cache; done; sync; echo 3 > /proc/sys/vm/drop_caches',
            ]
            self.run_sshcmds(self.nodes[host]['ip'], cmds, self.host_password)

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

    def deal_with_sarlog_cpu(self, host, casename, path):
        #%usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
        cpu_result = []
        cmd = 'grep "CPU      %usr" -A 1 {}/{}_sar.txt | grep all'.format(path, self.nodes[host]['ip'])
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
        cpu_result.append(self.get_average(cpu_result))
        return cpu_result

    def deal_with_sarlog_memory(self, host, casename, path):
        #kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
        mem_result = []
        with open('{}/{}_sar.txt'.format(path, self.nodes[host]['ip']), 'r') as f:
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
        mem_result.append(self.get_average(mem_result))
        return mem_result

    def get_network_device(self, host):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=self.nodes[host]['ip'], port=22, username='root', password=self.host_password)
        stdin, stdout, stderr = ssh.exec_command(
            'ifconfig | grep "inet " -B 1')
        result = stdout.read()
        ssh.close()

        results = result.split('--')
        for result in results:
            result = re.sub('\n', '', result)
            match = re.match('(\S+):.*inet (\S+) ', result)
            ip = match.group(2)
            if self.ip_in_subnet(ip, self.network['public_network']):
                public_n = match.group(1)
            elif self.ip_in_subnet(ip, self.network['cluster_network']):
                cluster_n = match.group(1)

        return cluster_n, public_n

    def deal_with_sarlog_nic(self, host, casename, path):
        #rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
        cluster_n, public_n = self.get_network_device(host)
        with open('{}/{}_sar.txt'.format(path, self.nodes[host]['ip']), 'r') as f:
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
        cluster_result.append(self.get_average(cluster_result))
        public_result.append(self.get_average(public_result))
        both_result['cluster_network:{}'.format(cluster_n)] = cluster_result
        both_result['public_network:{}'.format(public_n)] = public_result

        return both_result

    def get_average(self, results):
        total = {}
        num = 0
        for data in results:
            for key, value in data.items():
                if key == "time":
                    continue
                if not total.has_key(key):
                    total[key] = value
                    continue
                num =  num + 1
                total[key] = float(total[key]) + float(value)
        total[key] = total[key]/num
        total['avg'] = "True"
        return total

    def deal_with_sarlog(self, casename, path):
        all_result = {}
        for host in self.host_list:
            print datetime.datetime.now(),
            print "deal_with_sarlog_cpu"
            all_result[host] = self.deal_with_sarlog_cpu(host, casename, path)
        json.dump(all_result, open('{}/sar_cpu.json'.format(path), 'w'), indent=2)

        for host in self.host_list:
            print datetime.datetime.now(),
            print "deal_with_sarlog_memory"
            all_result[host] = self.deal_with_sarlog_memory(host, casename, path)
        json.dump(all_result, open('{}/sar_memory.json'.format(path), 'w'), indent=2)

        for host in self.host_list:
            print datetime.datetime.now(),
            print "deal_with_sarlog_nic"
            all_result[host] = self.deal_with_sarlog_nic(host, casename, path)
        json.dump(all_result, open('{}/sar_nic.json'.format(path), 'w'), indent=2)

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

    def deal_with_iostatlog(self, casename, path):
        #rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util

        all_result = {}
        for host in self.host_list:
            print datetime.datetime.now(),
            print "deal_with_iostatlog: {}".format(host)
            osd_result = {}

            with open('{}/{}_iostat.txt'.format(path, self.nodes[host]['ip'])) as f:
                time = f.readline()
            osd_result['start_time'] = re.search(' (\S*:.*:\S*) ', time).group(1)

            for osd_num,osd in self.nodes[host]['osd'].items():
                print datetime.datetime.now(),
                print "deal_with_iostatlog: {}".format(osd_num)
                oj_result = {}
                for disk_name,disk in osd.items():
                    print datetime.datetime.now(),
                    print "deal_with_iostatlog: {}".format(disk)
                    osd_disk = disk.split('/')[-1]
                    #osd_disk = re.match('/dev/(.*)', disk).group(1)
                    disk_result = []
                    cmd = 'grep "{}" {}/{}_iostat.txt'.format(osd_disk, path, self.nodes[host]['ip'])
                    disk_data_list = subprocess.check_output(cmd, shell=True).split('\n')
                    del disk_data_list[0]
                    del disk_data_list[-1]
                    n = 0
                    print datetime.datetime.now(),
                    print len(disk_data_list)
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
        json.dump(all_result, open('{}/iostat.json'.format(path), 'w'), indent=2)

    def deal_with_perfdumplog(self, casename, path):
        log_files = os.popen('ls {}/*ceph_perfdump.json'.format(path)).readlines()
        for log_file in log_files:
            log_file = log_file.strip()
            perfdump = json.load(open(log_file))
            log_file = log_file.split('/')[-1]
            host = log_file.split('_')[0]
            log_osd = log_file.split('_')[1]
            #self.db.insert_tb_perfdumpdata(casename, host, log_osd, **perfdump)
            dumpdata = json.dumps(perfdump)
            self.db.insert_tb_perfdumpdata(casename, host, log_osd, dumpdata)

    def deal_with_cephstatuslog(self, casename, path):
        log_file = '{}/{}_cephstatus.txt'.format(path, self.client)
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

    def deal_with_cephinfo(self, casename, path):
        ceph_info = {'monnum': self.monnum, 'nodenum': len(self.host_list)}

        version_file = '{}/{}_cephv.txt'.format(path, self.client)
        with open(version_file, 'r') as f:
            ceph_info['version'] = f.readline().strip()

        osdtree_file = '{}/{}_cephosdtree.json'.format(path, self.client)
        osdtree = json.load(open(osdtree_file))
        osdnum = 0
        for node in osdtree['nodes']:
            if node['type'] == 'osd':
                osdnum = osdnum + 1
        ceph_info['osdnum'] = osdnum
        #ceph_info.update(osdtree)

        df_file = '{}/{}_cephdf.json'.format(path, self.client)
        df = json.load(open(df_file))
        ceph_info.update(df)

        pools_info = self.get_pool_info(df['pools'])

        ceph_info['pool'] = pools_info
        json.dump(ceph_info, open('{}/ceph_info.json'.format(path), 'w'), indent=2)
        if self.havedb:
            self.db.insert_tb_cephinfo(casename, **ceph_info)
            for pool, pool_info in pools_info.items():
                self.db.insert_tb_poolinfo(casename, pool, **pool_info)

    def deal_with_sysdata_logfile(self, log_dir, sysdata_dir):
        path = '{}/{}'.format(log_dir, sysdata_dir)
        dir_list = path.split('/')
        casename = re.match('sysdata_(.*)', dir_list[-1]).group(1)

        print datetime.datetime.now(),
        print "deal_with_sarlog"
        self.deal_with_sarlog(casename, path)
        print datetime.datetime.now(),
        print "deal_with_iostatlog"
        #self.deal_with_iostatlog(casename, path)
        if self.havedb:
            print datetime.datetime.now(),
            print "deal_with_perfdumplog"
            self.deal_with_perfdumplog(casename, path)
            print datetime.datetime.now(),
            print "deal_with_cephstatuslog"
            self.deal_with_cephstatuslog(casename, path)
            print datetime.datetime.now(),
            print "deal_with_cephinfo"
            self.deal_with_cephinfo(casename, path)

    def format_subnet(self, subnet_input):
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
    
    def ip_in_subnet(self, ip, subnet):
        subnet = self.format_subnet(str(subnet))
        subnet_array = subnet.split("/")
        ip = self.format_subnet(ip + "/" + subnet_array[1])
        return ip == subnet
