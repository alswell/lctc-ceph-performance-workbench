import os
import sys
import argparse
import subprocess
import time
import shutil
import re
import yaml


def create_image(image_size, image_count, image_pool, client, client_password):
    exist_rbd_list = get_rbd_list(client, client_password)
    need_rbd_list = []
    for i in range(int(image_count)):
        rbd_name = 'testimage_{}_{}'.format(image_size, i)
        need_rbd_list.append(rbd_name)
        if exist_rbd_list.count(rbd_name) == 1:
            cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'rm', rbd_name]
            subprocess.check_call(cmd)
    
    for rbd in need_rbd_list:
        cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'create', rbd, '--image-format', '2', '--size', str(image_size), '--pool', image_pool]
        print subprocess.check_output(cmd)
        cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'info', '-p', image_pool, '--image', rbd]
        print subprocess.check_output(cmd)

def fullfill_file(image_size, image_count, image_pool):
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
            config_f.write("size={}M\n".format(image_size))
            config_f.write("group_reporting\n")
            config_f.write("[rbd_image{}]\n".format(i))
            config_f.write("rbdname=testimage_{}_{}\n".format(image_size, i))
    return dir_path

def fullfill(path, size, client, client_password):
    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'ps', '-ef']
    child1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    child2 = subprocess.Popen(["grep", "fio"],stdin=child1.stdout, stdout=subprocess.PIPE)
    child3 = subprocess.Popen(["grep", "server"],stdin=child2.stdout, stdout=subprocess.PIPE)
    output = child3.communicate()[0].replace('\n', '')
    if output == '':
        print "===={} without fio server".format(client)
        raise Exception("====Please run \"nohup fio --server &\" in {}".format(client))

        '''
        try:
            os.system("ssh -o StrictHostKeyChecking=no {} nohup fio --server &".format(client))
            time.sleep(5)
        except Exception, e:
            print e
            sys.exit(1)
        '''

    for config in os.listdir(path):
        cmd = ['fio', '--client', client, '{}/{}'.format(path, config)]
        print cmd
        child = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        while True:
            line = child.stdout.readline()
            if not line:
                break
            print line

    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'du']
    status = subprocess.check_output(cmd).split('\n')
    del status[0]
    del status[-1]
    del status[-1]
    for _status in status:
        match = re.match(r'([^\s]*)\s+([^\s]*)\s+([^\s]*)', _status)
        if re.match('testimage_{}'.format(size), match.group(1)):
           if match.group(2) != '{}M'.format(size):
                raise Exception("Error: image error, please check the image name.")
           if match.group(3) != '{}M'.format(size):
                raise Exception("full fill {} fail! The use size is {} which should be {}.".format(match.group(1), match.group(3), size))


def get_rbd_list(client, client_password):
    cmd = ['sshpass', '-p', client_password, 'ssh', '-o', 'StrictHostKeyChecking=no', client, 'rbd', 'list']
    rbds = subprocess.check_output(cmd)
    rbd_list =  rbds.split('\n')
    return rbd_list


def main():
    parser = argparse.ArgumentParser(
        prog="init_image",
        version='v0.1',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Create rbd image and full fill.")
    parser.add_argument('-C', '--client', dest="client",
                metavar="ceph client", action="store",
                    help='''ceph client''')
    parser.add_argument('-I', '--imagecount', dest="image_count",
                metavar="ceph rbd image count", action="store",
                    help='''ceph rbd image count''')
    parser.add_argument('-S', '--imagesize', dest="imagesize",
                metavar="ceph rbd image size", action="store",
                    help='''ceph rbd image size''')
    parser.add_argument('-P', '--pool', dest="pool",
                metavar="ceph pool name", action="store",
                    help='''ceph pool name''')
    args = parser.parse_args()

    image_size = [1024, 10240, 102400]
    client = args.client

    hwinfo_file = 'ceph_hw_info.yml'
    with open(hwinfo_file, 'r') as f:
        ceph_info = yaml.load(f)
    client_password = False
    if ceph_info['ceph-client'].has_key(client):
        client_ip = ceph_info['ceph-client'][client]['ip']
        client_password = ceph_info['ceph-client'][client]['password']
    else:
        for client_name, client_data in ceph_info['ceph-client'].items():
            if client == client_data['ip']:
                client_ip = client_data['ip']
                client_password = client_data['password']
    if not client_password:
        raise Exception("Error: can't find {} in ceph_hw_info.yml.".format(client))
    client_password = str(client_password)


    file_dir = fullfill_file(image_size[int(args.imagesize)-1], args.image_count, args.pool)

    create_image(image_size[int(args.imagesize)-1], args.image_count, args.pool, client_ip, client_password)
    fullfill(file_dir, image_size[int(args.imagesize)-1], client_ip, client_password)



if __name__ == '__main__':
    main()
