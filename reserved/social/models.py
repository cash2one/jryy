#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

class UserExtend(User):
    '''
    @des:注册邮箱验证程序
    '''
    email_code = models.CharField(max_length=60, blank=True, null=True, verbose_name=u"email验证码")
    rq = models.DateTimeField(auto_now_add=True,verbose_name=u"发送日期")
    sina_id = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"SINA ID")
    qq_id = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"QQ ID")
    is_shiming= models.BooleanField(default=False)

