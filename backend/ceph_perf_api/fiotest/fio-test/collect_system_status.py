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
import socket,struct


class SysInfo(object):

    def __init__(self, client, havedb=False):
        if havedb:
            from todb import ToDB
            self.db = ToDB()
        self.havedb = havedb
        self.intervaltime = 1
        self.ceph_intervaltime = 10

        self.client = client
        self.host_list = []
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=client, port=22, username='root', password='passw0rd')
        cmd = 'ceph osd tree | grep host'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.readlines()
        for item in output:
            match = re.search('host (\S*)\s+', item)
            self.host_list.append(match.group(1))

        self.nodes = get_ceph_config_file('/tmp/', client)['ceph-node']

    def run_sshcmds(self, host, cmds):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = 'passw0rd'
        )
        for cmd in cmds:
            print "exec {} in {}.".format(cmd, host)
            ssh.exec_command(cmd)
        ssh.close()

    def sys_info(self, host):
        cmds = [
            'sar -A {} >/tmp/sar.log &'.format(self.intervaltime),
            'date >/tmp/iostat.log; iostat -p -dxm {} >>/tmp/iostat.log &'.format(self.intervaltime),
        ]
        self.run_sshcmds(host, cmds)

    def get_sys_info(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            print 'get sysinfo {}'.format(host)
            p = Process(target=self.sys_info, args=(host_ip,))
            p.start()
        self.get_ceph_status(self.client)

    def get_ceph_status(self, client):
        cmds = [
            'date >/tmp/cephstatus.log; while true; do ceph -s --format json-pretty; sleep {}; done >>/tmp/cephstatus.log &'.format(self.ceph_intervaltime)]
        self.run_sshcmds(client, cmds)

    def cleanup_sys_info(self, host):
        cmds = [
            'kill -9 `ps -ef | grep sar | grep -v grep | awk \'{print $2}\'`',
            'kill -9 `ps -ef | grep iostat | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(host, cmds)

    def cleanup_all(self):
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            print 'cleanup sysinfo collect process in {}'.format(host)
            p = Process(target=self.cleanup_sys_info,args=(host_ip,))
            p.start()
        cmd = [
            'kill -9 `ps -ef | grep \'ceph -s\' | grep -v grep | awk \'{print $2}\'`',
        ]
        self.run_sshcmds(self.client, cmd)


    def get_logfile(self, host, log, log_dir):
        t = paramiko.Transport(host, "22")
        t.connect(username = "root", password = "passw0rd")
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
        self.get_logfile(host, 'sar.log', log_dir)
        self.get_logfile(host, 'iostat.log', log_dir)

    def get_all_host_logfile(self, log_dir):
        self.cleanup_all()
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            print 'get sysinfo logs from {}'.format(host)
            self.get_all_logfile(host_ip, log_dir)
            self.get_ceph_perfdump(host_ip, log_dir)
            self.get_ceph_conf(host_ip, log_dir)

        self.get_logfile(self.client, 'cephstatus.log', log_dir)

    def get_ceph_perfdump(self, host, log_dir):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = 'passw0rd'
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
        t.connect(username = "root", password = "passw0rd")
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
            self.run_sshcmds(self.nodes[host]['public_ip'], cmds)

    def get_ceph_conf(self, host, log_dir):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = host,
            port = 22,
            username = 'root',
            password = 'passw0rd'
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
        t.connect(username = "root", password = "passw0rd")
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

    def close_db(self):
        if self.havedb:
            self.db.close_db()

    def get_datetime_fordb_sarlog(self, time, t_type, casename):
        if t_type == 'PM':
            time_list = time.split(':')
            _time = '{}:{}:{}'.format(
                int(time_list[0]) + 12,
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
        cmd = 'grep "CPU      %usr" -A 1 {}_sar.log | grep all'.format(host)
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
        with open('{}_sar.log'.format(host), 'r') as f:
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

        ssh.connect(hostname=self.nodes[host]['public_ip'], port=22, username='root', password='passw0rd')
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
            elif self.nodes[host]['cluster_ip'] == ip:
                cluster_n = match.group(1)

        return cluster_n, public_n

    def deal_with_sarlog_nic(self, host, casename):
        #rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
        cluster_n, public_n = self.get_network_device(host)
        host = self.nodes[host]['public_ip']
        with open('{}_sar.log'.format(host), 'r') as f:
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

    def deal_with_sarlog(self, log_dir):
        dir_list = os.getcwd().split('/')
        casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)

        all_result = {}
        for host in self.host_list:
            all_result[host] = self.deal_with_sarlog_cpu(self.nodes[host]['public_ip'], casename)
        json.dump(all_result, open('./sar_cpu.json', 'w'), indent=2)

        for host in self.host_list:
            all_result[host] = self.deal_with_sarlog_memory(self.nodes[host]['public_ip'], casename)
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

    def deal_with_iostatlog(self, log_dir):
        #rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
        dir_list = os.getcwd().split('/')
        casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)

        all_result = {}
        for host in self.host_list:
            osd_result = {}

            with open('{}_iostat.log'.format(self.nodes[host]['public_ip'])) as f:
                time = f.readline()
            osd_result['start_time'] = re.search(' (\S*:.*:\S*) ', time).group(1)

            for osd_num,osd in self.nodes[host]['osd'].items():
                oj_result = {}
                for disk_name,disk in osd.items():
                    osd_disk = re.match('/dev/(.*)', disk).group(1)
                    disk_result = []
                    cmd = 'grep "{}" {}_iostat.log'.format(osd_disk, self.nodes[host]['public_ip'])
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
                            self.db.insert_tb_iostatdata(casename, host, osd_num, disk_name, **result)
                        n = n + self.intervaltime
                    oj_result[disk_name] = disk_result
                osd_result[osd_num] = oj_result
            all_result[host] = osd_result
        json.dump(all_result, open('./iostat.json', 'w'), indent=2)

    def deal_with_perfdumplog(self, log_dir):
        if self.havedb:
            dir_list = os.getcwd().split('/')
            casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)
            log_files = os.popen('ls *ceph_perfdump.json').readlines()
            for log_file in log_files:
                log_file = log_file.strip()
                host = log_file.split('_')[0]
                log_osd = log_file.split('_')[1]
                perfdump = json.load(open(log_file))
                self.db.insert_tb_perfdumpdata(casename, host, log_osd, **perfdump)

    def deal_with_cephconfiglog(self, log_dir):
        if self.havedb:
            dir_list = os.getcwd().split('/')
            casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)
            log_files = os.popen('ls *ceph_config.json').readlines()
            for log_file in log_files:
                log_file = log_file.strip()
                host = log_file.split('_')[0]
                osd = log_file.split('_')[1]
                ceph_configs = json.load(open(log_file))
                self.db.insert_tb_cephconfigdata(casename, host, osd, **ceph_configs)

    def deal_with_cephstatuslog(self, log_dir):
        if self.havedb:
            dir_list = os.getcwd().split('/')
            casename = re.match('sysinfo_(.*)', dir_list[-1]).group(1)
            log_files = os.popen('ls *cephstatus.log').readlines()
            log_file = log_files[0].strip()
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
                        with open('/tmp/ceph_tmp.log', 'w') as output_f:
                            for output_line in line_to_file:
                                output_f.write(output_line)
                        ceph_status = json.load(open('/tmp/ceph_tmp.log'))
                        ceph_mon = str(ceph_status['monmap']['mons'])
                        ceph_map = str(ceph_status['pgmap']['pgs_by_state'])
                        ceph_mon = re.sub('\'', '\\\'', ceph_mon)
                        ceph_map = re.sub('\'', '\\\'', ceph_map)
                        ceph_status['monmap']['mons'] = ceph_mon
                        ceph_status['pgmap']['pgs_by_state'] = ceph_map
                        self.db.insert_tb_cephstatusdata(casename, time, **ceph_status)

    def deal_with_sysinfo_logfile(self, log_dir):
        org_dir = os.getcwd()
        os.chdir(log_dir)
        self.deal_with_sarlog(log_dir)
        self.deal_with_iostatlog(log_dir)
        self.deal_with_cephconfiglog(log_dir)
        self.deal_with_perfdumplog(log_dir)
        self.deal_with_cephstatuslog(log_dir)
        os.chdir(org_dir)

def get_ceph_config_file(log_dir, client):
    t = paramiko.Transport(client, "22")
    t.connect(username = "root", password = "passw0rd")
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
    sysinfo = SysInfo(client)
    '''
    #sysinfo.get_sys_info()
    #sysinfo.cleanup_all()
    sysinfo.deal_with_sysinfo_logfile(
        sysinfo_dir,
    )
    '''
    sysinfo.deal_with_perfdumplog('/root/fio-zelin/test-suites/test2/log_2017_07_28_15_00_39/sysinfo_rbd_rw_4k_runtime30_iodepth1_numjob1_imagenum2_test2_%70_2017_07_28_15_00_39')

if __name__ == '__main__':
    main()
