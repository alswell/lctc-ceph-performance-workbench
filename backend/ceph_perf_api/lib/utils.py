import os
import paramiko
import yaml
import subprocess
import time
import re


HAVEDB = True
if HAVEDB:
    from fiotest.fio_test.todb import ToDB as FIODB
    from ITuning_ceph_deploy.ITuning_ceph_deploy.todb import ToDB as DEPLOYDB


class Utils(object):
    def __init__(self):
        self.havedb = HAVEDB
        if self.havedb:
            self.FioDB = FIODB
            self.DeployDB = DEPLOYDB
            self.fiodb = self.FioDB()
            self.deploydb = self.DeployDB()

    def ssh_cmd(self, user, host, cmd, password=None):
        cmd_ssh = "sshpass -p {} ssh -o StrictHostKeyChecking=no {}@{} '{}'".format(password, user, host, cmd)
        print(cmd_ssh)
        return subprocess.check_output(cmd_ssh, shell=True)

    def _run_sshcmds(self, host, cmds, password):
        for cmd in cmds:
            self.ssh_cmd('root', host, cmd, password=password)

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

    def checkandstart_fioser(self, client, password=None):
        output = ''
        while output == '':
            try:
                output = subprocess.check_output('sshpass -p {} ssh -o StrictHostKeyChecking=no {} ps -ef | grep fio | grep server | grep -v grep'.format(password, client), shell=True)
            except subprocess.CalledProcessError, result:
                output = result.output
                if result.output == '' and result.returncode == 1:
                    print "===={} without fio server".format(client)
                    cmd = "sshpass -p {} ssh {} 'fio --server >/dev/null 2>&1 &'".format(password, client)
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

