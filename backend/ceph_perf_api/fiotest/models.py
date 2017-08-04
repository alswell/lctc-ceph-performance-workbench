# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):  # 必须继承models.Model
    # 不写则，django默认创建ID列，自增，主键
    # 用户名列，字符串类型，指定长度
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

