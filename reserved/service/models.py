#coding:utf-8
from django.contrib.auth.models import User
from django.db import models

class SerMerchant(models.Model):
    """
    服务机构、美容院
    """
    mer_name = models.CharField(u'服务机构名称',max_length=200)
    mer_address = models.CharField(u'经营地址', max_length=200)
    mer_bizhour = models.CharField(u'经营时间', max_length=200)
    mer_img =  models.ImageField(upload_to='./upload/merchant/', height_field=600, width_field=300, max_length=200, blank=True)
    mer_tel = models.CharField(u'预约电话', max_length=200)
    mer_weibo = models.CharField(u'官方微博', max_length=200)
    mer_weixin = models.CharField(u'官方微信', max_length=200)
    mer_detail = models.CharField(u'详细介绍', max_length=200)
    mer_founder = models.ForeignKey(User)

    def __unicode__(self):
        return self.mer_name

    class Meta:
        verbose_name_plural = '美容院'

class ServiceType(models.Model):
    """
        项目分类
    """
    merchant = models.ForeignKey(SerMerchant)
    tp_name = models.CharField(u'类型名称', max_length=200)
    tp_desc = models.TextField(u'详细描述')

    def __unicode__(self):
        return self.tp_name

    class Meta:
        verbose_name_plural = '项目分类'

class Service(models.Model):
    """
        服务项目
    """
    merchant = models.ForeignKey(SerMerchant)
    ch_name = models.CharField(u'服务名', max_length=200)
    en_name = models.CharField(u'英文', max_length=200)
    ser_img =  models.ImageField(u'图片',upload_to='/Users/linzerd/github/jryy/reserved', height_field=600, width_field=300, max_length=200, blank=True)
    ser_type = models.ForeignKey(ServiceType,verbose_name=u'类别')
    time_spent = models.IntegerField(u'周期时间', default=0) # default minute unit
    ser_desc = models.TextField(u'项目描述')
    create_time = models.DateField(u'创建时间', auto_now_add=True)
    update_time = models.DateField(u'创建时间', auto_now=True)

    def __unicode__(self):
        return self.ch_name

    class Meta:
        verbose_name_plural = '服务项目'

class SerRoom(models.Model):
    """
    美容房间
    """
    merchant = models.ForeignKey(SerMerchant)
    rm_name = models.CharField(u'房间名', max_length=200)
    rm_img =  models.ImageField(upload_to='./upload/rooms/', height_field=600, width_field=300, max_length=200, blank=True)
    support_service = models.ManyToManyField(Service)
    detail = models.TextField(u'房间详情')

    def __unicode__(self):
        return self.rm_name

    class Meta:
        verbose_name_plural = '房间'

class Beautician(models.Model):
    """
    美容师
    """
    GENDER_CHOICES = (
        (0, u'女'),
        (1, u'男'),
        )

    merchant = models.ForeignKey(SerMerchant)
    bc_name = models.CharField(u'姓名', max_length=200)
    nickname = models.CharField(u'昵称', max_length=200)
    bc_img =  models.ImageField(upload_to='/Users/linzerd/github/jryy/reserved/upload', max_length=200, blank=True)
    gender = models.IntegerField(u'性别', default=0, choices=GENDER_CHOICES)
    age = models.IntegerField(u'年龄', default=20)
    level = models.IntegerField(u'等级', default=20)
    detail = models.TextField(u'详情')
    goodat = models.ManyToManyField(Service)   # 擅长项目

    class Meta:
        verbose_name_plural = '美容师'

    def __unicode__(self):
        return self.bc_name
