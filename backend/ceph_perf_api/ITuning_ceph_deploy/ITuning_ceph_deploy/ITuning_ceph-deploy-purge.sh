#!/bin/bash


# The sh file runs on admin node
#
# The args format:
#   ./my_ceph-deploy-purge.sh <cluster_name> <host_list>
#   host_list: host_name in host_list split joint by ','
#
# example:
#   ./my_ceph-deploy-purge.sh mycluster1 ceph-1,ceph-2,ceph-3,client1


function error_check {
    if [ "$?" != "0" ]; then
        exit
    fi 
}


if [ ! $2 ]; then
    echo "usage: my_ceph-deploy-purge.sh <cluster_name> <host_list>"
    exit
fi


DIR_MYCLUSTER=/home/$1


cd $DIR_MYCLUSTER

host_list=`echo $2 | sed 's/,/ /g'`

for host in $host_list
do
    ssh ${host} killall -9 ceph-osd
    ssh ${host} killall -9 ceph-mon
    ceph-deploy purge ${host}
    error_check
    ceph-deploy purgedata ${host}
    error_check
done

ceph-deploy forgetkeys
error_check


rm -rf ceph*
