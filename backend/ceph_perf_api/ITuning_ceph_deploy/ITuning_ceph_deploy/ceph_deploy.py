import subprocess
import re
import sys
import datetime
import time
import os
import json
from lib.utils import Utils


class Deploy(Utils):
    def __init__(self):
        super(Deploy, self).__init__()
        self.file_path = os.path.dirname(os.path.realpath(__file__))

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
        cluster_info = {'status': "initenv"}
        self.deploydb.update_cluster(clusterid, **cluster_info)
        cmd = "sshpass -p {} ssh-copy-id -o StrictHostKeyChecking=no {}".format(password, ip)
        print datetime.datetime.now(),
        print cmd
        subprocess.check_call(cmd, shell=True)
    
        cmds = [
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
        osds = ','.join(osd_list)
        mons = ','.join(mon_list)
        disks = ','.join(disk_list)
        clients = ','.join(client_list)
    
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        cluster_info = {'status': "Deploying", 'create_time': create_time}
        self.deploydb.update_cluster(clusterid, **cluster_info)
    
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
        self.deploydb.update_cluster(clusterid, **cluster_info)
    
    def purge(self, clusterid, name, hostnames):
        cluster_info = {'status': "purge"}
        self.deploydb.update_cluster(clusterid, **cluster_info)
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

    def get_default_cephconfig(self, clusterid, host, password):
        cmd = 'sshpass -p {} ssh {} find /var/run/ceph -name \'*osd*asok\''.format(password, host)
        print cmd
        output = subprocess.check_output(cmd, shell=True).split('\n')
        osd = re.search('(osd\.\d+)', output[0]).group(1)
        cmd = "sshpass -p {} ssh {} 'ceph --admin-daemon {} config show > /tmp/{}_ceph_config.json'".format(password, host, output[0], clusterid)
        print cmd
        output = subprocess.check_output(cmd, shell=True)
        cmd = 'sshpass -p {} scp {}:/tmp/{}_ceph_config.json {}/../../'.format(
            password, host, clusterid, self.file_path)
        print cmd
        subprocess.check_call(cmd, shell=True)
        ceph_configs = json.load(
            open('{}/../../{}_ceph_config.json'.format(self.file_path, clusterid))
        )
        dumpdata = json.dumps(ceph_configs)
        dumpdata = re.sub('\\\\', '\\\\\\\\', dumpdata)

        self.deploydb.insert_cephconfig(clusterid, host, osd, dumpdata)

        cmd = 'sshpass -p {} scp {}:/etc/ceph/ceph.conf {}/../../{}_ceph.conf'.format(
            password, host, self.file_path, clusterid)
        print cmd
        subprocess.check_call(cmd, shell=True)

