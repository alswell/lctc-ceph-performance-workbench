#!/bin/bash


# The sh file runs on admin node.
#
# Prepare:
#   1. ceph osd pool created.
#
# The args format:
#   ./ITuning_ceph_osd_manage.sh <-o osd_operation> <-l host_disk_journal_list/osd_num_list/host_osd_list> [-c cluster_name]
#   1. osd_operation: support 5 operations: create, in/out, up/down.
#   2. host_disk_journal_list/osd_num_list/host_osd_list:
#      2.1 create
#          host_disk_journal_list: host:disk:journal combination in host_disk_journal_list split joint by ','.
#                                  host:disk:journal format: host_name:disk_name:journal_disk_path. "ceph-3:vdb:/dev/sdb" eg.
#      2.2 in/out
#          osd_num_list: osd_num in osd_num_list split joint by ','.
#                        you can get osd_num by execute cmd "ceph osd tree", osd.{osd_num} in the rank "NAME".
#      2.3 up/down
#          host_osd_list: host:osd_num combination in host_osd_list split joint by ','.
#                         host:osd_num format: host_name:osd_num. "ceph-3:2" eg.
#   3. cluster_name: when operation is "create", cluster_name is needed.
#
# Example:
#   ./ITuning_ceph_osd_manage.sh -o create -l ceph-1:vdc:/dev/sdc,ceph-3:vdb:/dev/sdb -c mycluster
#   or
#   ./ITuning_ceph_osd_manage.sh -o in -l 0,1
#   or
#   ./ITuning_ceph_osd_manage.sh -o up -l ceph-1:0,ceph-2:1


function error_check {
    if [ "$?" != "0" ]; then
        exit
    fi
}

function osd_create() {
    if [ ! $2 ]; then
        echo "usage: ./ITuning_ceph_osd_manage.sh -o create <-l host_disk_journal_list> <-c cluster_name>"
        exit
    fi

    cd /home/$2


    host_disk_journal_list=`echo $1 | sed 's/,/ /g'`
    host_journal_list=""

    for item in $host_disk_journal_list
    do
        OIFS=$IFS; IFS=":"; set -- $item; osds_host_name=$1;osds_disk=$2;osds_journal=$3; IFS=$OIFS

        sudo ceph-deploy disk zap ${osds_host_name}:${osds_disk}

        for host_journal in $host_journal_list
        do
            if [ ${host_journal} == ${osds_host_name}:${osds_journal} ]; then
                continue 2
            fi
        done

        sudo ceph-deploy disk zap ${osds_host_name}:${osds_journal}
        host_journal_list="${host_journal_list} ${osds_host_name}:${osds_journal}"
    done

    for item in $host_disk_journal_list
    do
        sudo ceph-deploy osd prepare --filestore $item
        error_check
    done
}

function osd_in() {
    osd_num_list=`echo $1 | sed 's/,/ /g'`

    for osd_num in $osd_num_list
    do
        sudo ceph osd in $osd_num
    done
}

function osd_out() {
    osd_num_list=`echo $1 | sed 's/,/ /g'`

    for osd_num in $osd_num_list
    do
        sudo ceph osd out $osd_num
    done
}

function osd_up() {
    host_osd_list=`echo $1 | sed 's/,/ /g'`

    for item in $host_osd_list
    do
        OIFS=$IFS; IFS=":"; set -- $item; host_name=$1;osd_num=$2; IFS=$OIFS

        ssh ${host_name} sudo systemctl start ceph-osd@${osd_num}
    done
}

function osd_down() {
    host_osd_list=`echo $1 | sed 's/,/ /g'`

    for item in $host_osd_list
    do
        OIFS=$IFS; IFS=":"; set -- $item; host_name=$1;osd_num=$2; IFS=$OIFS

        ssh ${host_name} sudo systemctl stop ceph-osd@${osd_num}
    done
}


if [ ! $4 ]; then
    echo "usage: ./ITuning_ceph_osd_manage.sh <-o osd_operation> <-l host_disk_journal_list/osd_num_list/host_osd_list> [-c cluster_name]"
    exit
fi

echo $*
# get the arguments
while getopts :o:l:c: value
do
    case $value in
        o )
            my_operation=$OPTARG
            ;;
        l )
            my_list=$OPTARG
            ;;
        c )
            my_cluster=$OPTARG
            ;;
        ? )
            echo "$OPTARG error!"
            exit 1;;
    esac
done


case $my_operation in
    create)
        osd_create $my_list $my_cluster
        ;;
    in)
        osd_in $my_list
        ;;
    out)
        osd_out $my_list
        ;;
    up)
        osd_up $my_list
        ;;
    down)
        osd_down $my_list
        ;;
    * )
        echo "Error! Unknow operation $my_operation!"
        exit 1;;
esac
