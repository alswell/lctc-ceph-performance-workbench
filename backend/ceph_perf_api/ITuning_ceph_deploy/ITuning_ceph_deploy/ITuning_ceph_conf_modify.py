# The python file runs on admin node.
#
# The args format:
#   python ./ITuning_ceph_conf_modify.py <source_path> <dest_path>
#   source_path: the source is the conf file user defined. user defined conf file should have the same format as ceph.conf.
#
# Example:
#   python ./ITuning_ceph_conf_modify.py /home/new_conf/my_ceph.conf /home/mycluster/ceph.conf
 
 
import ConfigParser
 
def main(args):
    my_config = ConfigParser.ConfigParser()
    ceph_config = ConfigParser.ConfigParser()
 
    my_config.read(args[0])
    ceph_config.read(args[1])
 
    my_secs = my_config.sections()
    ceph_secs = ceph_config.sections()
 
    for my_sec in my_secs:
        my_opts = my_config.options(my_sec)
 
        if my_sec not in ceph_secs:
            ceph_config.add_section(my_sec)
 
            for my_opt in my_opts:
                my_val = my_config.get(my_sec, my_opt)
                ceph_config.set(my_sec, my_opt, my_val)
        else:
            ceph_opts = ceph_config.options(my_sec)

            for my_opt in my_opts:
                my_val = my_config.get(my_sec, my_opt)
 
                if my_opt in ceph_opts:
                    ceph_config.set(my_sec, my_opt, my_val)
                else:
                    my_space_opt = my_opt.replace('_', ' ')
                    my_uline_opt = my_opt.replace(' ', '_')
                    if my_space_opt in ceph_opts:
                        ceph_config.set(my_sec, my_space_opt, my_val)
                    elif my_uline_opt in ceph_opts:
                        ceph_config.set(my_sec, my_uline_opt, my_val)
                    else:
                        ceph_config.set(my_sec, my_opt, my_val)

    # write to file
    ceph_config.write(open(args[1], "r+"))


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
