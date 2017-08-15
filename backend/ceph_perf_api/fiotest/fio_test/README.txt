# fio-test


5.5.52-MariaDB
yum install -y gcc python-devel python-pip mysql mysql-devel mariadb-server mariadb

systemctl start mariadb
systemctl enable mariadb

# create database
mysql
MariaDB [(none)]> insert into mysql.user(Host,User,Password) values('localhost','test',password('1234'));
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> drop database fiotest;
MariaDB [(none)]> create database fiotest;
MariaDB [(none)]> grant all privileges on fiotest.* to test@localhost identified by '1234';
MariaDB [(none)]> exit;

# create tables
python todb.py
OR
./manage.py makemigrations fiotest
./manage.py migrate fiotest


# install dependenies
yum install gcc
pip install --upgrade pip
pip install -r requirement.txt

# install fio
#  update ceph repo
/etc/yum.repos.d/ceph.repo
[Ceph]
name=Ceph packages for $basearch
baseurl=http://download.ceph.com/rpm-jewel/el7/$basearch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
priority=1

[Ceph-noarch]
name=Ceph noarch packages
baseurl=http://download.ceph.com/rpm-jewel/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
priority=1

[ceph-source]
name=Ceph source packages
baseurl=http://download.ceph.com/rpm-jewel/el7/SRPMS
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
priority=1

# install dependenies  :   gcc librbd1-devel
yum install -y librbd1-devel gcc

# compile fio 2.21
unzip fio-fio-2.21.zip
cd fio-fio-2.21
./configure
make
make install
ln -s /usr/local/bin/fio /usr/bin/fio

# check fio verion
fio -v
fio-2.21



#
./run-fio [init-image|build-suite|list-suites|run $suitename $jobname [--nodb]]

For the new ceph env, please run "init-image" to create new rbds for testing.
Or use "build-suite" to create new test config file for FIO.
Or use "list-suites" to show the previous created test.
Or use "run $suitename $jobname" to run test.

