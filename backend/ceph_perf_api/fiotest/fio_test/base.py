import os
import yaml
import paramiko
import re
from lib.utils import Utils


class FioBase(Utils):
    def __init__(self, test_path, clusterid):
        super(FioBase, self).__init__()

        self.test_path = test_path
        self.clusterid = clusterid
        file_path = os.path.dirname(os.path.realpath(__file__))
        hwinfo_file = '{}/../../{}_ceph_hw_info.yml'.format(file_path, clusterid)
        with open(hwinfo_file, 'r') as f:
            ceph_info = yaml.load(f)

        self.clients = ceph_info['ceph-client']
        self.nodes = ceph_info['ceph-node']
        self.network = ceph_info['ceph-network']

        self.client_password = False
        with open('{}/fioserver_list.conf'.format(test_path), 'r') as f:
            clients = f.readlines()
            client = clients[0].strip()

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
