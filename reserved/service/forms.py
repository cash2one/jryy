#!/usr/bin/env python
#coding=utf-8
import re

from django import forms
from django.contrib.auth.models import User
#from django.utils.translation import gettext_lazy as _
from django.db.models import ObjectDoesNotExist

from service.models import Service
from orders.models import Order

def _(msg):
    return msg

my_messages={'required':_(u'输入不能为空'),'max_length':_(u'请输入正确的手机号')}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=11, label=u'用户名', required=True, error_messages=my_messages)
    password = forms.CharField(max_length=24, label=u'密码', required=True, widget=forms.PasswordInput, error_messages=my_messages)

    def clean_username(self):
        try:
            username = self.data.get('username')
            m = re.search(u'[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]+', username)
            if m and m.group(0):
                user = User.objects.get(email=m.group(0))
            else:
                user = User.objects.get(username=self.data.get('username'))
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('该用户不存在'))
        if user.is_active:
            return user.username
#        else:
#            raise forms.ValidationError(_('该用户不存在'))

    def clean_password(self):
        try:
            from django.contrib.auth import authenticate
            user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
            if not user:
                raise forms.ValidationError(_('用户名或密码错误'))
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('用户名或密码错误'))
        return self.data.get('password')

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ('merchant',)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('merchant',)



#    ch_name = forms.CharField(max_length=100 ,label='服务机构名称')
#    en_name = forms.CharField(max_length=200, label='英文名称')
#    ser_img = forms.ImageField(label='图片')
#    ser_type = forms.ChoiceField(label='留言内容',widget=forms.Textarea)
#    time_spent = forms.BooleanField(required=False ,label='订阅该贴')
#    ser_desc = forms.BooleanField(required=False ,label='订阅该贴')
