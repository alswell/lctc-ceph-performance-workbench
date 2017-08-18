1. How to run django server:
    cd ceph_perf_api
    ./manage.py runserver <IP>:<PORT>  # example: ./manage.py runserver 0.0.0.0:8866

2. Django ORM (mysql):
http://blog.csdn.net/fgf00/article/details/53678205
http://www.cnblogs.com/caseast/articles/4806213.html
  1) initial
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

  2) add table
    vim mysql/models.py
        # edit table
    ./manage.py makemigrations mysql    #初始化表结构
    ./manage.py migrate                 #表创建完毕

3. 
 yum install rabbitmq-server
