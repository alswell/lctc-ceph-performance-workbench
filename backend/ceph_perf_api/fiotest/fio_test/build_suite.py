import os
import sys
import argparse
import datetime
import shutil
import subprocess
import re
import json
import copy


class FIOTest(object):

    def create_suite_dir(self, suitename):
        time = str(datetime.datetime.now())
        create_time = re.sub('\.\d+', '', time)
        current_date = re.sub('\s', '', time)
        suitename = re.sub('_', '', suitename)
        suitename = suitename + '_' + current_date
        file_path = os.path.dirname(os.path.realpath(__file__))
        suite_dir = "{}/../../test-suites/{}".format(file_path, suitename)
        path = "{}/config".format(suite_dir)
        print "=================================="
        print "test suite dir is: {}".format(suite_dir)
        print "=================================="
        if os.path.exists(suite_dir):
            shutil.rmtree(suite_dir)
        os.makedirs(path)
        return suite_dir, create_time
    
    def case(
        self,
        path,
        casenum,
        pool,
        rw,
        bs,
        runtime,
        iodepth,
        numjobs,
        image_num,
        suitename,
        rwmixread,
        imagename,
        clientslist,
        other_fio_config
    ):
        suitename = re.sub('_', '', suitename)
        for i in range(len(clientslist)):
            config_para = 'case'+str(casenum)+'_pool'+pool+'_'+rw+'_'+bs+'_runtime'+runtime+'_iodepth'+iodepth+'_numjob'+numjobs+'_imagenum'+image_num+'_'+suitename+'_%'+rwmixread+'_'+str(i)
            for fioconfig in other_fio_config:
                 fioconfig = re.sub('=', '', fioconfig)
                 #config_para = config_para + '_' + fioconfig
            config_filename = config_para+'.config'
            with open('{}/config/{}'.format(path, config_filename), 'aw') as f:
                f.write("[global]\n")
                f.write("ioengine=rbd\n")
                f.write("clientname=admin\n")
                f.write("pool={}\n".format(pool))
                f.write("rw={}\n".format(rw))
                f.write("bs={}\n".format(bs))
                f.write("runtime={}\n".format(runtime))
                f.write("iodepth={}\n".format(iodepth))
                f.write("numjobs={}\n".format(numjobs))
                f.write("direct=1\n")
                f.write("randrepeat=0\n")
                f.write("rwmixread={}\n".format(rwmixread))
                f.write("new_group\n")
                f.write("group_reporting\n")
                for fioconfig in other_fio_config:
                    f.write("{}\n".format(fioconfig))
                # $image_start $image_end: Different fio server run in different image
                image_start = i*int(image_num)
                image_end = image_start + int(image_num)
                for n in range(image_start, image_end):
                    f.write("[rbd_image{}]\n".format(n))
                    f.write("rbdname={}_{}\n".format(imagename, n))
    
    def gen_setup_ceph_config(self, path, cephconfig_list):
        if cephconfig_list[0] != 'default':
            result_ceph_configs = []
            for raw_ceph_config in cephconfig_list:
                match = re.search('\[(\d+)-(\d+)\]', raw_ceph_config)
    
                result_ceph_config = {}
                ceph_config_list = raw_ceph_config.split(';')
                if ceph_config_list[-1] == '':
                    del ceph_config_list[-1]
                n = 0
    
                if match:
                    range_ceph_configs = []
                    range_dic = {}
                    normal_dic = {}
                    for ceph_config in ceph_config_list:
                        match_range = re.match('(.*)=(\[\d+-\d+\])', ceph_config)
                        if match_range:
                            range_dic[match_range.group(1)] = match_range.group(2)
                        else:
                            match_normal = re.match('(.*)=(.*)', ceph_config)
                            normal_dic[match_range.group(1)] = match_range.group(2)
                    range_ceph_configs.append(normal_dic)
                    while len(range_dic) > 0:
                        key, value = range_dic.popitem()
                        range_match = re.match('\[(\d+)-(\d+)\]', value)
                        _range_ceph_configs = []
                        for org_ceph_config in range_ceph_configs:
                            for range_num in range(int(range_match.group(1)), int(range_match.group(2))+1):
                                org_dic = copy.deepcopy(org_ceph_config)
                                org_dic[key] = range_num
                                _range_ceph_configs.append(org_dic)
                        range_ceph_configs = _range_ceph_configs
                    result_ceph_configs = result_ceph_configs + range_ceph_configs
                else:
                    for ceph_config in ceph_config_list:
                        match = re.match('(.*)=(.*)', ceph_config)
                        if match:
                            result_ceph_config[match.group(1)] = match.group(2)
                        else:
                            raise Exception("ceph config format incorrect: {}".format(ceph_config))
                    result_ceph_configs.append(result_ceph_config)
            json.dump(result_ceph_configs, open('{}/setup_ceph_config.json'.format(path), 'w'), indent=2)
    
            return result_ceph_configs
