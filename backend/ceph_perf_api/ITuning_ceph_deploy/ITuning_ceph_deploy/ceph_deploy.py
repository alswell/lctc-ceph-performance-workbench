import subprocess
import re
import sys
import argparse
import pexpect
import datetime
import time
import os


def ssh_cmd(user, ip, cmd):
    cmd_ssh = "ssh -o StrictHostKeyChecking=no {}@{} \"{}\"".format(user, ip, cmd)
    print(cmd_ssh)
    return subprocess.check_output(cmd_ssh, shell=True)

def check_vm_status(ip):
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

def init(ip, password, hostname):
    cmd = "sshpass -p {} ssh-copy-id -o StrictHostKeyChecking=no {}".format(password, ip)
    print datetime.datetime.now(),
    print cmd
    subprocess.check_call(cmd, shell=True)

    cmds = [
        'setenforce 0',
        '/bin/cp -f /etc/sysconfig/selinux .',
        'sed -i \"s/SELINUX=enforcing/SELINUX=disabled/g\" selinux',
        '/bin/cp -f selinux /etc/sysconfig/selinux',
        'hostnamectl set-hostname {}'.format(hostname),
        'systemctl disable firewalld.service',
        'systemctl stop firewalld.service',
        #'reboot',
    ]
    for cmd in cmds:
        print datetime.datetime.now(),
        print ssh_cmd('root', ip, cmd)

    '''
    if check_vm_status(ip):
        pass
    else:
        print "boot up {} time out!".format(ip)
        sys.exit(1)
    '''

    dep_p = ['epel-release']
    for p in dep_p:
        cmd = "ssh -o StrictHostKeyChecking=no {} yum install -y {}".format(hostname, p)
        print datetime.datetime.now(),
        print cmd
        subprocess.check_call(cmd, shell=True)


    find = False
    with open('/etc/hosts', 'r') as f:
        with open('/tmp/hosts', 'w') as output:
            for line in f:
                if re.search(ip, line):
                    if re.search(hostname, line):
                        output.write(line)
                        find = True
                    else:
                        print "Error: Find Another hostname in /etc/hosts with {}".format(ip)
                        sys.exit(1)
                else:
                    output.write(line)
            if not find:
                output.write('\n{} {}'.format(ip, hostname))

    print datetime.datetime.now(),
    print "Updated /etc/hosts."
    open('/etc/hosts', "wb").write(open('/tmp/hosts', "rb").read())

def deploy(name, mon_list, osd_list, disk_list, client_list, conf):
    #./ITuning_ceph-deploy.sh -n mycluster1 -m ceph-1 -o ceph-1,ceph-2,ceph-3 -d ceph-1:/dev/sda:/dev/sdc,ceph-2:/dev/sda:/dev/sdc,ceph-3:sda:/dev/sdb -c client-1 -f /root/lctc-ceph-performance-workbench/backend/ceph_perf_api/ITuning_ceph_deploy/ITuning_ceph_deploy/ITuning_ceph.conf
    osds = ','.join(osd_list)
    mons = ','.join(mon_list)
    disks = ','.join(disk_list)
    clients = ','.join(client_list)

    cmd = "./ITuning_ceph-deploy.sh -n {} -m {} -o {} -d {} -c {} -f {}".format(
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

def purge(name, hostnames):
    hosts = ','.join(hostnames)

    print os.getcwd()
    cmd = "./ITuning_ceph-deploy-purge.sh {} {}".format(name, hosts)
    print datetime.datetime.now(),
    print cmd
    subprocess.check_call(cmd, shell=True)

def createrbdpool(osdnum, client):
    pgsize = osdnum*100/3
    cmd = "ceph osd pool create rbd {}".format(pgsize)
    print datetime.datetime.now(),
    ssh_cmd('root', client, cmd)


def main():

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
    #    init(ips[i], password, hostnames[i])

    purge(name, hostnames)
    deploy(name, mon_list, osdhost_list, disk_list, client_list, conf)
    createrbdpool(len(disk_list), client_list[0])
    

if __name__ == '__main__':
    main()

