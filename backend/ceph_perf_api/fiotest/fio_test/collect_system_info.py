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
from collect_system_data import SysData


class SysInfo(SysData):

    def get_hwinfo_log(self, host_ip, log_dir):
        cmds = [
            'dmidecode >/tmp/dmidecode.txt',
            'cat /proc/meminfo >/tmp/meminfo.txt',
            'cat /proc/cpuinfo >/tmp/cpuinfo.txt',
            'lsblk >/tmp/lsblk.txt',
        ]
        self.run_sshcmds(host_ip, cmds, self.host_password)

        self.get_logfile(host_ip, self.host_password, 'dmidecode.txt', log_dir)
        self.get_logfile(host_ip, self.host_password, 'meminfo.txt', log_dir)
        self.get_logfile(host_ip, self.host_password, 'cpuinfo.txt', log_dir)
        self.get_logfile(host_ip, self.host_password, 'lsblk.txt', log_dir)

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
            print cmd
            ssh.exec_command(cmd)
            ceph_config_file_list.append('{}_ceph_config.json'.format(
                re.search('(osd\.\d+)', osd).group(1)
            ))
        ssh.close()

        time.sleep(1)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        for log in ceph_config_file_list:
            remotepath = '/tmp/{}'.format(log)
            localpath = '{}/{}_{}'.format(log_dir, host, log)
            cmd = ['sshpass', '-p', self.host_password, 'scp',
                '-o', 'StrictHostKeyChecking=no', '-r',
                'root@{}:{}'.format(host, remotepath), localpath]
            print cmd
            subprocess.check_call(cmd)

    def get_all_host_sysinfo_logfile(self, log_dir):
        for host in self.host_list:
            host_ip = self.nodes[host]['public_ip']
            self.get_hwinfo_log(host_ip, log_dir)
            self.get_ceph_conf(host_ip, log_dir)

    def deal_with_cephconfiglog(self, jobid, path):
        log_files = os.popen('ls {}/*ceph_config.json'.format(path)).readlines()
        for log_file in log_files:
            log_file = log_file.strip()
            ceph_configs = json.load(open(log_file))
            log_file = log_file.split('/')[-1]
            host = log_file.split('_')[0]
            osd = log_file.split('_')[1]
            self.db.insert_tb_cephconfigdata(jobid, host, osd, **ceph_configs)

    def deal_with_smartctl(self, result):
        model = ''
        speed = ''
        for line in result:
            model_match = re.match('Device Model:\s+(.*)$', line)
            speed_match = re.match('Rotation Rate:\s+(.*)$', line)
            if model_match:
                model = model_match.group(1)
            if speed_match:
                speed = speed_match.group(1)
        return model, speed

    def deal_with_lsblk_log(self, jobid, path):
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
 
            with open('{}/{}_lsblk.txt'.format(path, ip), 'r') as f:
                f.readline()
                for line in f.readlines():
                    match = re.match('(\w+)\s+\S+\s+\S+\s+(\S+)', line)
                    if match:
                        disk_name = match.group(1)
                        disk_size = match.group(2)
                        cmd = 'smartctl -i /dev/{}'.format(disk_name)
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        smartctl = stdout.read()
                        disk_model, disk_speed = self.deal_with_smartctl(smartctl.split('\n'))

                        cmd = 'cat /sys/block/{}/queue/read_ahead_kb'.format(disk_name)
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        output = stdout.read()
                        read_ahead_kb = re.sub('\n', '', output)

                        cmd = 'cat /sys/block/{}/queue/scheduler'.format(disk_name)
                        stdin, stdout, stderr = ssh.exec_command(cmd)
                        output = stdout.read()
                        scheduler = re.sub('\n', '', output)
                        
                        with open('{}/{}_{}_diskinfo.txt'.format(path, ip, disk_name), 'w') as diskinfo_f:
                            diskinfo_f.write(smartctl)
                            diskinfo_f.write(read_ahead_kb)
                            diskinfo_f.write(scheduler)

                        if self.havedb:
                            self.db.insert_tb_diskinfo(
                                jobid,
                                host,
                                disk_name,
                                disk_size,
                                disk_model,
                                disk_speed,
                                read_ahead_kb,
                                scheduler,
                            )
            ssh.close()


    def deal_with_cpuinfo_log(self, path):
        cpu_info = {}
        for host in self.host_list:
            with open('{}/{}_cpuinfo.txt'.format(path, self.nodes[host]['public_ip']), 'r') as f:
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

    def deal_with_meminfo_log(self, path):
        mem_info = {}
        for host in self.host_list:
            with open('{}/{}_dmidecode.txt'.format(path, self.nodes[host]['public_ip']), 'r') as f:
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
            with open('{}/{}_meminfo.txt'.format(path, self.nodes[host]['public_ip']), 'r') as f:
                for line in f:
                    maxsize_match = re.match('MemTotal:\s+(.*)$', line)
                    if maxsize_match:
                        memsize = maxsize_match.group(1)
            mem_info[host] = {'memtype': mem_M+':'+mem_S, 'totalsize': memsize, 'memnum': memnum}
        return mem_info 

    def deal_with_hwinfo(self, jobid, path):
        cpu_info = self.deal_with_cpuinfo_log(path)
        mem_info = self.deal_with_meminfo_log(path)
        for host in self.host_list:
            hw_info = {}
            hw_info.update(cpu_info[host])
            hw_info.update(mem_info[host])
            hw_info.update(self.nodes[host]['hwinfo'])
            json.dump(hw_info, open('{}/{}_hw_info.json'.format(path, host), 'w'), indent=2)
            if self.havedb:
                self.db.insert_tb_hwinfo(jobid, host, **hw_info)

    def get_network_mtu(self, host):
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
            match = re.match('(\S+):.*mtu (\d+)\s+inet (\S+) ', result)
            ip = match.group(3)
            if self.ip_in_subnet(ip, self.network['public_network']):
                public_mtu = match.group(1)+":"+match.group(2)
            elif self.ip_in_subnet(ip, self.network['cluster_network']):
                cluster_mtu = match.group(1)+":"+match.group(2)

        return cluster_mtu, public_mtu

    def get_os_info(self, jobid, path):
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

            cmd = 'cat /proc/sys/kernel/pid_max'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read()
            os_info['PIDnumber'] = re.sub('\n', '', output)

            cluster_mtu, public_mtu = self.get_network_mtu(host)
            os_info['PublicMTU'] = public_mtu
            os_info['ClusterMTU'] = cluster_mtu

            #os_info.update(self.nodes[host]['osinfo'])

            json.dump(os_info, open('{}/{}_os_info.json'.format(path, host), 'w'), indent=2)
            if self.havedb:
                self.db.insert_tb_osinfo(jobid, host, **os_info)

    def deal_with_sysinfo_logfile(self, sysinfo_dir, jobid):
        dir_list = sysinfo_dir.split('/')

        if self.havedb:
            self.deal_with_cephconfiglog(jobid, sysinfo_dir)
        self.deal_with_lsblk_log(jobid, sysinfo_dir)
        self.deal_with_hwinfo(jobid, sysinfo_dir)
        self.get_os_info(jobid, sysinfo_dir)


def get_ceph_config_file_sds(log_dir, client):
    t = paramiko.Transport(client, "22")
    t.connect(username = "root", password = self.client_password)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath = '/etc/ceph/ceph.conf'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

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
