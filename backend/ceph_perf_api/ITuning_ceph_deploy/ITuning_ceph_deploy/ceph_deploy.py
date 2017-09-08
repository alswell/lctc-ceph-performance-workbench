import subprocess
import re
import sys
import argparse
import pexpect
import datetime
import time
import os
from todb import ToDB


class Deploy(object):
    def __init__(self):
        self.file_path = os.path.dirname(os.path.realpath(__file__))

    def ssh_cmd(self, user, ip, cmd):
        cmd_ssh = "ssh -o StrictHostKeyChecking=no {}@{} \"{}\"".format(user, ip, cmd)
        print(cmd_ssh)
        return subprocess.check_output(cmd_ssh, shell=True)
    
    def check_vm_status(self, ip):
        ping_vm = ['ping', '-c', '3', ip]
        timeout = 600
        time_start = time.time()
        while True:
            try:
                subprocess.check_call(ping_vm)
            except:
                time.sleep(10)
                if time.time() - time_start > timeout:
                    return False
            else:
                return True
    
    def initenv(self, clusterid, ip, password, hostname):
        db = ToDB()
        cluster_info = {'status': "initenv"}
        db.update_cluster(clusterid, **cluster_info)
        cmd = "sshpass -p {} ssh-copy-id -o StrictHostKeyChecking=no {}".format(password, ip)
        print datetime.datetime.now(),
        print cmd
        subprocess.check_call(cmd, shell=True)
    
        cmds = [
            #'setenforce 0',
            '/bin/cp -f /etc/sysconfig/selinux .',
            'sed -i \"s/SELINUX=enforcing/SELINUX=disabled/g\" selinux',
            '/bin/cp -f selinux /etc/sysconfig/selinux',
            'hostnamectl set-hostname {}'.format(hostname),
            'systemctl disable firewalld.service',
            'systemctl stop firewalld.service',
        ]
        for cmd in cmds:
            print datetime.datetime.now(),
            print self.ssh_cmd('root', ip, cmd)

        find = False
        with open('/etc/hosts', 'r') as f:
            with open('/tmp/hosts', 'w') as output:
                for line in f:
                    if re.search(ip, line):
                        if re.search(hostname, line):
                            output.write(line)
                            find = True
                        else:
                            raise Exception("Error: Find Another hostname in /etc/hosts with {}".format(ip))
                    else:
                        output.write(line)
                if not find:
                    output.write('\n{} {}'.format(ip, hostname))
    
        print datetime.datetime.now(),
        print "Updated /etc/hosts."
        open('/etc/hosts', "wb").write(open('/tmp/hosts', "rb").read())
    
        dep_p = ['epel-release', 'net-tools', 'sysstat']
        for p in dep_p:
            cmd = "ssh -o StrictHostKeyChecking=no {} yum install -y {}".format(hostname, p)
            print datetime.datetime.now(),
            print cmd
            subprocess.check_call(cmd, shell=True)
    
    def deploy(self, clusterid, name, mon_list, osd_list, disk_list, client_list, conf):
        db = ToDB()
        osds = ','.join(osd_list)
        mons = ','.join(mon_list)
        disks = ','.join(disk_list)
        clients = ','.join(client_list)
    
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        cluster_info = {'status': "Deploying", 'create_time': create_time}
        db.update_cluster(clusterid, **cluster_info)
    
        cmd = "{}/ITuning_ceph-deploy.sh -n {} -m {} -o {} -d {} -c {} -f {}".format(
            self.file_path,
            name,
            mons,
            osds,
            disks,
            clients,
            conf,
        )
        print datetime.datetime.now(),
        print cmd
        subprocess.check_call(cmd, shell=True)
    
        cmd = "ceph health"
        status = self.ssh_cmd('root', client_list[0], cmd)
        cluster_info = {'health': status, 'status': 'Deploy Finished'}
        db.update_cluster(clusterid, **cluster_info)
    
    def purge(self, clusterid, name, hostnames):
        db = ToDB()
        cluster_info = {'status': "purge"}
        db.update_cluster(clusterid, **cluster_info)
        hosts = ','.join(hostnames)
    
        print os.getcwd()
        cmd = "{}/ITuning_ceph-deploy-purge.sh {} {}".format(self.file_path, name, hosts)
        print datetime.datetime.now(),
        print cmd
        subprocess.check_call(cmd, shell=True)
    
    def createrbdpool(self, osdnum, host):
        pgsize = osdnum*100/3
        cmds = [
            "ceph osd pool create rbd {}".format(pgsize),
            "ceph osd pool application enable rbd rbd",
        ]
        for cmd in cmds:
            print datetime.datetime.now(),
            self.ssh_cmd('root', host, cmd)

    def reboot(self, hostname):
        cmd = "ssh -o StrictHostKeyChecking=no {} reboot".format(hostname)
        print datetime.datetime.now(), cmd
        subprocess.call(cmd, shell=True)
        time.sleep(3)
        if self.check_vm_status(hostname):
            time.sleep(2)
        else:
            raise Exception("boot up {} time out!".format(hostname))

    def checkandstart_fioser(self, hostname):
        output = ''
        while output == '':
            try:
                cmd = 'ssh -o StrictHostKeyChecking=no {} ps -ef | grep fio | grep server | grep -v grep'.format(hostname)
                print cmd
                output = subprocess.check_output(cmd, shell=True)
            except subprocess.CalledProcessError, result:
                output = result.output
                if result.output == '' and result.returncode == 1:
                    cmd = "ssh client-1 'fio --server >/dev/null 2>&1 &'".format(hostname)
                    print cmd
                    subprocess.call(cmd, shell=True)
                    time.sleep(1)
                    continue
                else:
                    raise Exception(result)
            else:
                match = re.match('\S+\s+(\d+)', output)
                process_id = match.group(1)
                print "process_id: {}".format(process_id)

    def install_fio(self, hostname):
        dep_p = ['librbd1-devel', 'gcc', 'unzip']
        for p in dep_p:
            cmd = "ssh -o StrictHostKeyChecking=no {} yum install -y {}".format(hostname, p)
            print datetime.datetime.now(), cmd
            subprocess.check_call(cmd, shell=True)

        cmd = "scp {}/../../fiotest/fio_test/fio-fio-2.21.zip {}:/root/".format(self.file_path, hostname)
        print datetime.datetime.now(), cmd
        subprocess.check_call(cmd, shell=True)

        cmds = [
            'rm -rf fio-fio-2.21',
            'unzip fio-fio-2.21.zip',
            'cd fio-fio-2.21; ./configure',
            'cd fio-fio-2.21; make',
            'cd fio-fio-2.21; make install',
            'rm -f /usr/bin/fio',
            'ln -s /usr/local/bin/fio /usr/bin/fio',
            'fio --version',
        ]
        for cmd in cmds:
            print datetime.datetime.now(),
            print self.ssh_cmd('root', hostname, cmd)


    def gen_yaml_file(self,
        clusterid,
        disk_list,
        osdhost_list,
        nodeips,
        nodepw_list,
        client_list,
        clientips,
        clientpw_list,
        public_network,
        cluster_network,
    ):
        with open('{}/../../{}_ceph_hw_info.yml'.format(self.file_path, clusterid), 'w') as f:
            osdnum = 0
            f.write("ceph-client:\n")
            for i in range(len(client_list)):
                f.write("  {}:\n".format(client_list[i]))
                f.write("    ip: {}\n".format(clientips[i]))
                f.write("    user: root\n")
                f.write("    password: {}\n".format(clientpw_list[i]))
            f.write("ceph-node:\n")
            for i in range(len(osdhost_list)):
                f.write("  {}:\n".format(osdhost_list[i]))
                f.write("    ip: {}\n".format(nodeips[i]))
                f.write("    user: root\n")
                f.write("    password: {}\n".format(nodepw_list[i]))
                f.write("    osd:\n")
                for disk in disk_list:
                    disk_info = disk.split(':')
                    if disk_info[0] == osdhost_list[i]:
                        f.write("      osd.{}:\n".format(osdnum))
                        f.write("        osd-disk: {}\n".format(disk_info[1]))
                        f.write("        journal-disk: {}\n".format(disk_info[2]))
                        osdnum = osdnum + 1
                f.write("    hwinfo:\n")
                f.write("      HyperThreading:\n")
                f.write("      VirtualTechnology:\n")
                f.write("      NUMA:\n")
                f.write("      OperatingModes:\n")
                f.write("    osinfo:\n")
            f.write("ceph-network:\n")
            f.write("  public_network: {}\n".format(public_network))
            f.write("  cluster_network: {}\n".format(cluster_network))

def main():
    deploy = Deploy()

    ips = ['192.168.230.218', '192.168.230.201', '192.168.230.196', '192.168.230.199']
    password = 'passw0rd'
    name = "mycluster1"
    osdhost_list = ['ceph-3', 'ceph-1', 'ceph-2']
    client_list = ['client-1']

    mon_list = [osdhost_list[1]]
    disk_list = [osdhost_list[1]+':/dev/sda:/dev/sdc', osdhost_list[2]+':/dev/sda:/dev/sdc', osdhost_list[0]+':sda:/dev/sdb']   

    hostnames = osdhost_list + client_list

    public_network = '192.168.230.0/24'
    cluster_network = '192.168.220.0/24'
    objectstore = 'filestore'
    journal_size = 10240

    with open('/tmp/ITuning_ceph.conf', 'w') as f:
        f.write('[global]\n')
        f.write('public_network = {}\n'.format(public_network))
        f.write('cluster_network = {}\n'.format(cluster_network))
        f.write('osd objectstore = {}\n'.format(objectstore))
        f.write('[osd]\n')
        f.write('osd journal size = {}\n'.format(journal_size))

    conf = '/tmp/ITuning_ceph.conf'

    #for i in range(len(ips)):
    #    deploy.init(ips[i], password, hostnames[i])

    #deploy.purge(name, hostnames)
    #deploy.deploy(name, mon_list, osdhost_list, disk_list, client_list, conf)
    #deploy.createrbdpool(len(disk_list), client_list[0])
    #deploy.reboot('ceph-1')
    deploy.checkandstart_fioser('client-1')
    

if __name__ == '__main__':
    main()

