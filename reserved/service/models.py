#coding:utf-8
from django.contrib.auth.models import User
from django.db import models

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper



class SerMerchant(models.Model):
    """
    服务机构、美容院
    """
    mer_name = models.CharField(u'服务机构名称',max_length=200)
    mer_address = models.CharField(u'经营地址', max_length=200)
    mer_bizhour = models.CharField(u'经营时间', max_length=200)
    mer_img =  models.ImageField(upload_to=path_and_rename('merchant'), max_length=200, blank=True)
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

import os
from uuid import uuid4

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
    bc_img =  models.ImageField(upload_to=path_and_rename('beauticians'), blank=True)
    gender = models.IntegerField(u'性别', default=0, choices=GENDER_CHOICES)
    age = models.IntegerField(u'年龄', default=20)
    level = models.IntegerField(u'等级', default=20)
    detail = models.TextField(u'详情')
    goodat = models.ManyToManyField(Service)   # 擅长项目

    class Meta:
        verbose_name_plural = '美容师'

    def __unicode__(self):
        return self.bc_name

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
         
        # If there is no image associated with this.
        # do not create thumbnail
         
        import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
         
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200,200)
        if not self.bc_img:
            return
        DJANGO_TYPE = self.bc_img.file.content_type
         
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
         
        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.bc_img.read()))
         
        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #
        # I commented this part since it messes up my png files
        #
        #if image.mode not in ('L', 'RGB'):
        # image = image.convert('RGB')
         
        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
         
        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
         
        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.bc_img.name)[-1],
        temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        # self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
         
    def save(self):
        # create a thumbnail
        self.create_thumbnail()
        super(type(self), self).save()

class CardPool(models.Model):
    USE_STATUS = (
            (0, u'未激活'),
            (1, u'已激活'),
            )

    CARD_STATUS = (
            (0, u'未激活'),
            (1, u'已激活'),
            )

    merchant = models.ForeignKey(SerMerchant)
    cardnu = models.CharField(u'卡号', max_length=22, blank=True)
    phoneno = models.CharField(u'手机号', max_length=22, blank=True)
    member_name = models.CharField(u'姓名', max_length=22, blank=True)
    user_status = models.IntegerField(u'激活状态', default=0, choices=USE_STATUS)
    card_status = models.IntegerField(u'状态', default=0, choices=CARD_STATUS)
    consume_time = models.DateTimeField(u'激活时间', blank=True, null=True)
    add_time = models.DateTimeField(u'创建时间', auto_now_add=True, blank=True)
    update_time = models.DateTimeField(u'创建时间', auto_now_add=True, blank=True)

