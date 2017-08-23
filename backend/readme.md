#### run server
```
cd ceph_perf_api
```
- How to run django server:
```
./manage.py runserver <IP>:<PORT>  # example: ./manage.py runserver 0.0.0.0:8866
```
or
```
.run_django.sh
```

- run job conductor(RPC server):
```
./run_job_conductor.py
```
- run all servers:
```
./run_all.sh
```
***
#### Django ORM (mysql):
- http://blog.csdn.net/fgf00/article/details/53678205
- http://www.cnblogs.com/caseast/articles/4806213.html
##### initial
```
    pip install MySQL-python
    ./manage.py startapp mysql
    vim ceph_perf_api/settings.py
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'mysql',            # 这里添加app
        ]
        DATABASES = {           # mysql
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'mydatabase',      # example: 'test'
                'USER': 'mydatabaseuser',  # example: 'root'
                'PASSWORD': 'mypassword',  # example: ''
                'HOST': '127.0.0.1',
                'PORT': '3306',
            }
        }
    vim mysql/models.py
        # edit table
    ./manage.py makemigrations mysql    #初始化表结构
    ./manage.py migrate                 #表创建完毕
```
##### add table
```
    vim mysql/models.py
        # edit table
    ./manage.py makemigrations mysql    #初始化表结构
    ./manage.py migrate                 #表创建完毕
```
***
#### Install Rabbitmq
```
    yum install rabbitmq-server
    service rabbitmq-server restart
```

