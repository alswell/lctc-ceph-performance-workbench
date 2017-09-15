# lctc-ceph-performance-workbench
#### Ceph performance test workbench for LCTC

- LCTC test team need a workbench to test ceph performance via GUI, which may support auto-deployment, parameter-setting and etc.
- We will lauch a project: lctc-ceph-performance-workbench, which is a website.
- The architecture of website mainly consists of separated frontend(Reactor) and backend(Django), frontend is responsible for GUI, and backend is responsible for data. Frontend send HTTP request to backend to fetch JSON data.

# install dependenies
```
yum install -y rabbitmq-server supervisor gcc python-devel python-pip mysql mysql-devel mariadb-server mariadb
pip install -r backend/requirements.txt

systemctl restart mariadb
systemctl enable mariadb

systemctl restart rabbitmq-server
systemctl enable rabbitmq-server

cp django.ini frontend.ini  job_conductor.ini /etc/supervisord.d/
supervisord -c /etc/supervisord.conf
supervisorctl update
supervisorctl reload
```

# create database
```
mysql
MariaDB [(none)]> insert into mysql.user(Host,User,Password) values('localhost','test',password('1234'));
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> drop database fiotest;
MariaDB [(none)]> create database fiotest;
MariaDB [(none)]> grant all privileges on fiotest.* to test@localhost identified by '1234';
MariaDB [(none)]> exit;
```

