#!/bin/bash


# The sh file runs on admin node.
#
# Prepare:
#   1. Set password free landing on mon_nodes, osd_nodes and client_nodes to the deploy node.
#   2. User defined ceph_conf_file is needed. See the file ITuning_ceph.conf.example.
#
# The args format:
#   ./my_ceph-deploy.sh <-n cluster_name> <-m mon_list> <-o osd_node_list> <-d host_disk_journal_list> [-c client_list] [-f ceph_conf_file]
#   mon_list: host_name in mon_list split joint by ','.
#   osd_node_list: host_name in osd_node_list split joint by ','.
#   host_disk_journal_list: host:disk:journal combination in host_disk_journal_list split joint by ',';
#                           host:disk:journal format: host_name:disk_name:journal_disk_path. "ceph-3:vdb:/dev/sdb" eg.
#   client_list: host_name in client_list split joint by ','.
#   ceph_conf_file: conf format in the file is a 'key = value' per line.
#
# Example:
#   ./my_ceph-deploy.sh -n mycluster1 -m ceph-1,ceph-2 -o ceph-1,ceph-2,ceph-3 -d ceph-1:vdc:/dev/sdc,ceph-3:vdb:/dev/sdb -c client1,client2 -f /root/ccz/a.conf


function error_check {
    if [ "$?" != "0" ]; then
        exit
    fi
}

function ceph_deploy_prepare {
    # disable SELINUX
    sudo setenforce 0

    sudo yum install yum-plugin-priorities

}


if [ ! $8 ]; then
    echo "usage: my_ceph-deploy.sh <-n cluster_name> <-m mon_list> <-o osd_node_list> <-d host_disk_journal_list> [-c client_list] [-f ceph_conf_file]"
    exit
fi

echo $*
# get the optional arguments
while getopts :n:m:o:d:c:f: value
do
    case $value in
        n )
            mycluster=$OPTARG
            ;;
        m )
            mon_list=`echo $OPTARG | sed 's/,/ /g'`
            ;;
        o )
            osd_node_list=`echo $OPTARG | sed 's/,/ /g'`
            ;;
        d )
            host_disk_journal_list=`echo $OPTARG | sed 's/,/ /g'`
            ;;
        c )
            client_list=`echo $OPTARG | sed 's/,/ /g'`
            ;;
        f )
            myconf_file=$OPTARG
            ;;
        ? )
            echo "$OPTARG error!"
            exit 1;;
    esac
done

DIR_MYCLUSTER=/home/${mycluster}


ceph_deploy_prepare


# ceph deploy tool install
yum install -y ceph-deploy
error_check


# ceph mon
if [ -d ${DIR_MYCLUSTER} ]; then
    cd ${DIR_MYCLUSTER}    
    rm -rf ceph*
else
    mkdir ${DIR_MYCLUSTER}
    cd ${DIR_MYCLUSTER}
fi

ceph-deploy new $mon_list
error_check


# modify ceph.conf
cat ${myconf_file} | sed -n '2,$p' >> ${DIR_MYCLUSTER}/ceph.conf


# get deploy_list and mgr_list
deploy_list=${mon_list}

for osd_node in $osd_node_list
do
    for mon_node in $mon_list
    do
        if [ ${mon_node} == ${osd_node} ]; then
            continue 2
        fi
    done

    deploy_list="${deploy_list} $osd_node"
done

mgr_list=${deploy_list}

for client_node in $client_list
do
    deploy_list="${deploy_list} $client_node"
done


# ceph deploy rpm packet install
export CEPH_DEPLOY_REPO_URL=http://mirrors.163.com/ceph/rpm-luminous/el7/
export CEPH_DEPLOY_GPG_URL=http://mirrors.163.com/ceph/keys/release.asc

ceph-deploy install ${deploy_list}
error_check


# mon initial
ceph-deploy mon create-initial
error_check

# manager create
ceph-deploy mgr create ${mgr_list}
error_check

# ceph config syn
ceph-deploy --overwrite-conf admin ${deploy_list}
error_check


# osds create
host_journal_list=""

for item in $host_disk_journal_list
do
    OIFS=$IFS; IFS=":"; set -- $item; osds_host_name=$1;osds_disk=$2;osds_journal=$3; IFS=$OIFS

    ceph-deploy disk zap ${osds_host_name}:${osds_disk}

    for host_journal in $host_journal_list
    do
        if [ ${host_journal} == ${osds_host_name}:${osds_journal} ]; then
            continue 2
        fi
    done

    ceph-deploy disk zap ${osds_host_name}:${osds_journal}
    host_journal_list="${host_journal_list} ${osds_host_name}:${osds_journal}"
done

for item in $host_disk_journal_list
do
    ceph-deploy osd prepare --filestore $item
    error_check
done
