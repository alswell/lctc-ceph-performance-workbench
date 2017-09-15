import os
import sys
import argparse
import subprocess
import time
import shutil
import re
import yaml


def create_image(image_name, image_size, image_count, image_pool, client, client_password):
    exist_rbd_list = get_rbd_list(client, client_password)
    need_rbd_list = []
    for i in range(int(image_count)):
        rbd_name = '{}_{}'.format(image_name, i)
        need_rbd_list.append(rbd_name)
        if exist_rbd_list.count(rbd_name) == 1:
            cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'rm', rbd_name]
            subprocess.check_call(cmd)
    
    for rbd in need_rbd_list:
        cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'create', rbd, '--image-format', '2', '--size', str(image_size), '--pool', image_pool]
        print subprocess.check_output(cmd)
        cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'info', '-p', image_pool, '--image', rbd]
        print subprocess.check_output(cmd)

def fullfill_file(image_name, image_size, image_count, image_pool):
    dir_path = '{}/full_fill/'.format(os.getcwd())
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)

    for i in range(int(image_count)):
        with open('{}/test{}'.format(dir_path, i), 'aw') as config_f:
            config_f.write("[global]\n")
            config_f.write("ioengine=rbd\n")
            config_f.write("clientname=admin\n")
            config_f.write("pool={}\n".format(image_pool))
            config_f.write("rw=write\n")
            config_f.write("bs=4M\n")
            config_f.write("iodepth=1024\n")
            config_f.write("numjobs=1\n")
            config_f.write("direct=1\n")
            config_f.write("size={}\n".format(image_size))
            config_f.write("group_reporting\n")
            config_f.write("[rbd_image{}]\n".format(i))
            config_f.write("rbdname={}_{}\n".format(image_name, i))
    return dir_path

def fullfill(path, image_name, size, client, client_password):
    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'ps', '-ef']
    child1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    child2 = subprocess.Popen(["grep", "fio"],stdin=child1.stdout, stdout=subprocess.PIPE)
    child3 = subprocess.Popen(["grep", "server"],stdin=child2.stdout, stdout=subprocess.PIPE)
    output = child3.communicate()[0].replace('\n', '')
    if output == '':
        print "===={} without fio server".format(client)
        os.system("sshpass -p {} ssh -o StrictHostKeyChecking=no {} 'fio --server >/dev/null 2>&1 &'".format(client_password, client))
        time.sleep(1)

    for config in os.listdir(path):
        cmd = ['fio', '--client', client, '{}/{}'.format(path, config)]
        print cmd
        child = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        while True:
            line = child.stdout.readline()
            if not line:
                break
            print line
            sys.stdout.flush()

    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'du']
    status = subprocess.check_output(cmd).split('\n')
    del status[0]
    del status[-1]
    del status[-1]
    match_size = re.match('(\d+)([GM])', size)
    if match_size.group(2) == 'G':
        size = int(match_size.group(1)) * 1024
    for _status in status:
        match = re.match(r'([^\s]*)\s+([^\s]*)\s+([^\s]*)', _status)
        if re.match('{}'.format(image_name), match.group(1)):
            size_match = re.match('(\d+)([GM])', match.group(2))
            if size_match.group(2) == 'G':
                total_size = int(size_match.group(1)) * 1024
            else:
                total_size = int(size_match.group(1))
            if total_size != size:
                raise Exception("Error: image error, please check the image name.")
    
            size_match = re.match('(\d+)([GM])', match.group(3))
            if size_match.group(2) == 'G':
                fill_size = int(size_match.group(1)) * 1024
            else:
                fill_size = int(size_match.group(1))
    
            if fill_size != size:
                raise Exception("full fill {} fail! The use size is {} which should be {}.".format(match.group(1), match.group(3), size))


def get_rbd_list(client, client_password):
    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'list']
    rbds = subprocess.check_output(cmd)
    rbd_list =  rbds.split('\n')
    return rbd_list
