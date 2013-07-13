#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

from django.db import models
from django.contrib.auth.models import User
from service.models import Service, SerRoom, Beautician

class Customer(models.Model):
    """
    顾客信息
    """

    GENDER_CHOICES = (
        (0, u'女'),
        (1, u'男'),
        )

    user = models.ForeignKey(User)
    nickname = models.CharField(u'顾客姓名', max_length=200)
    member_level = models.IntegerField(u'会员级别', default=0)
    gender = models.IntegerField(u'性别', default=0, choices=GENDER_CHOICES)
    age = models.IntegerField(u'年龄', default=20)

    def __unicode__(self):
        return nickname

    class Meta:
        verbose_name_plural = '顾客'



class Order(models.Model):
    """
    已成订单
    """
    ORDER_STATES = (
            (0, u'未知'),
            (1, u'新建'),
            (2, u'提交'),
            (3, u'确认'),
            (4, u'更改'),
            (5, u'进行'),
            (6, u'完成'),
            (7, u'评价'),
            (11, u'取消'),
            )

    user = models.ForeignKey(User)
    person = models.IntegerField(u'预约人数', default=1)
    order_begin = models.DateField(u'开始时间')
    order_end = models.DateField(u'结束时间')
    order_room = models.ForeignKey(SerRoom)    # 预约房间
    order_beautician = models.ForeignKey(Beautician)    # 预约美容师
    

    order_state = models.IntegerField(u'订单状态', default=0)
    create_time = models.DateField(u'创建时间', auto_now_add=True) 
    update_time = models.DateField(u'创建时间', auto_now_add=True) 
    
    class Meta:
        verbose_name_plural = '订单'

class OrderDetail(models.Model):
    """
    订单详情
    """
    orderid = models.ForeignKey(Order)    
    service = models.ForeignKey(Service)
    beautician = models.ForeignKey(Beautician)
    unit = models.IntegerField(u'预约时间', default=0)

    class Meta:
        verbose_name_plural = '订单'


class CustomerPreference(models.Model):
    """
    顾客偏好
    """
    customer = models.ForeignKey(Customer) 
    fav_beautician = models.ForeignKey(Beautician)
    fav_Service = models.ManyToManyField(Service)
    fav_SerRoom = models.ForeignKey(SerRoom)
    update_time = models.DateField(u'更新时间', auto_now=True)

    class Meta:
        verbose_name_plural = '顾客偏好'


class OrderComment(models.Model):
    """
    订单评论
    """
    order = models.ForeignKey(Order)
    score = models.IntegerField(u'分数', default=0)
    content = models.CharField(u'评论', max_length=300)
    create_time = models.DateField(u'评价时间', auto_now=True)

    class Meta:
        verbose_name_plural = '订单评论'

class BeauticianComment(models.Model):
    """
    美容师评价
    """
    order = models.ForeignKey(Order)
    beautician = models.ForeignKey(Beautician)
    score = models.IntegerField(u'分数', default=0)
    content = models.CharField(u'评论', max_length=300)
    create_time = models.DateField(u'评价时间', auto_now=True)

    class Meta:
        verbose_name_plural = '美容师评价'
