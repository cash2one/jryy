#!/usr/bin/env python
#coding=utf-8

import datetime
import random
import json

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.db.models.query import QuerySet
from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from service.models import Service, ServiceType, Beautician, SerMerchant, SerRoom, CardPool
from orders.models import Order

def toJSON(obj):
   if isinstance(obj, QuerySet):
       return simplejson.dumps(obj, cls=DjangoJSONEncoder)
   if isinstance(obj, models.Model):
       #do the same as above by making it a queryset first
       set_obj = [obj]
       set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)))
       #eliminate brackets in the beginning and the end
       str_obj = set_str[1:len(set_str)-2]
   return str_obj

def calendar(request):
    """
    第一页 选择预约日期
    """
    now = datetime.datetime.now()
    print now.isoweekday()
    start = now - datetime.timedelta(now.isoweekday())
    weeks = []
    for i in range(0, 6):
        days = []
        for j in range(0, 7):
            day_data = {}
            day = start + datetime.timedelta(days=7 * i + j)
            day_data['datedata'] = day
            day_data['order_status'] = random.randint(0, 2)
            if now > day:
                day_data['today_tag'] = -1
            elif now < day:
                day_data['today_tag'] = 1
            else:
                day_data['today_tag'] = 0

            days.append(day_data)
            #print days[i].day
        weeks.append(days)
    return render_to_response('client/calendar.html', {'weeks':weeks}, context_instance=RequestContext(request))

def day_detail(request, datestr):
    """
    第二页 选择时间
    """
    query_date = datetime.datetime.strptime(datestr, '%Y%m%d')
    now = datetime.datetime.now()
    open_hour = 10
    open_time = query_date + datetime.timedelta(seconds=60*60*10)
    close_hour = 22
    close_time = query_date + datetime.timedelta(seconds=60*60*22)
    step = (close_hour - open_hour) * 2
    day_status = []
    orders = Order.objects.filter(order_begin__gte=query_date.strftime('%Y-%m-%d 00:00:00'), order_end__lt=(query_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))
    print orders
    for i in range(0, step):
        daydata = {}
        this_time = open_time + datetime.timedelta(seconds=60*30*i)
        orders = Order.objects.filter(order_begin__lte=this_time, order_end__gt=this_time + datetime.timedelta(seconds=60*30))
        # 订单数量 和 美容师 数量进行比较
        if orders.count() == 1:
            status = 1
        elif orders.count() > 1:
            status = 2
        else:
            status = 0
        daydata['status'] = status
        daydata['time'] = this_time
        day_status.append(daydata)
        print status

    return render_to_response('client/day.html', {'day_status': day_status, 'query_date': query_date}, context_instance=RequestContext(request))

def choose_service(request, datestr, timestr):
    """
    选择项目
    """
    query_time = datetime.datetime.strptime(datestr + timestr, '%Y%m%d%H%M')
    sertps = ServiceType.objects.all()
    service_data = []
    for tps in sertps:
        tmp_service = {}
        tmp_service['type'] = tps
        typservices = Service.objects.filter(ser_type=tps)
        tmp_service['services'] = typservices
        service_data.append(tmp_service)
    #json_data = toJSON(service_data)

    context = {
        'services': service_data,
        'query_date_str': datestr,
        'query_time_str': timestr,
        'query_time': query_time,
        }
    return render_to_response('client/project.html', context, context_instance=RequestContext(request))


def order(request, datestr, timestr, service):
    """
    预订操作, 选择美容技师
    """
    query_time = datetime.datetime.strptime(datestr + timestr, '%Y%m%d%H%M')
    avi_beauticians = []
    orders = Order.objects.filter(order_begin__gte=query_time.strftime('%Y-%m-%d 00:00:00'), order_end__lt=(query_time + datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))
    beauticians = Beautician.objects.filter(merchant__id = 1)
    for btc in beauticians:
        orders = Order.objects.filter(merchant = btc, order_begin__gte=query_time.strftime('%Y-%m-%d %H:%M:00'), order_end__lt=(query_time + datetime.timedelta(seconds=60*60)).strftime('%Y-%m-%d %H:%M:00'))
        if orders.count() > 0:
            continue
        avi_beauticians.append(btc)
    print avi_beauticians

    context = {
        'avi_btcs': avi_beauticians,
        'query_date_str': datestr,
        'query_time_str': timestr,
        'query_time': query_time,
        }

    return render_to_response('client/beautician.html', context, context_instance=RequestContext(request))

def social_login(request):
    openid = request.POST.get('openid')
    nickname = request.POST.get('nickname')
    avatar = request.POST.get('avatar')
    social = request.POST.get('platform')
    ret = {}
    ret['ret'] = 0
    ret['msg'] = 'login ok'
    return HttpResponse(json.dumps(ret), mimetype='application/json')


def project(request):
    """
    预订操作, 选择项目
    """
    context = {
        'query_time': '',
        }

    return render_to_response('client/project.html', context, context_instance=RequestContext(request))

@csrf_exempt
def init(request):
    mobile = request.POST.get('mobile', '-1')
    user = User.objects.filter(username=mobile)
    ret = {}
    if user.count() > 0:
        ret['ret'] = 0
        ret['msg'] = 'already user'
    else:
        members = CardPool.objects.filter(phoneno=mobile)
        if members.count() > 0:
            ret['ret'] = 1
            ret['msg'] = 'u r a member not actived'
        else:
            ret['ret'] = -1
            ret['msg'] = 'u can do nothing here'
    return HttpResponse(json.dumps(ret), mimetype='application/json')

@csrf_exempt
def login(request):
    mobile = request.POST.get('mobile', '-1')
    password = request.POST.get('password', '-1')

    user = User.objects.filter(username=mobile)
    ret = {}
    if user.count() > 0:
        from django.contrib.auth import authenticate, login
        print newuser.username, userform.cleaned_data['password']
        #import pdb
        #pdb.set_trace()
        user = authenticate(username=mobile, password=password)
        if not user:
            ret['ret'] = -1
            ret['msg'] = 'error pass'
        else:
            login(request, user)
            ret['ret'] = 0
            ret['msg'] = 'login ok'
    else:
        members = CardPool.objects.filter(phoneno=mobile)
        if members.count() > 0:
            user = User(
                username = data['mobile'],
                mobile = data['mobile'],
                email = ''+data['mobile'] + '@qfpay.com',
                user_type = ut,
                state = 1,
                is_staff = False,
                is_active = True,
                is_superuser = False,
                last_login = now,
                date_joined = now,
                user_level = userlevel
            )
            user.set_password(password)
            user.save()

            if user.pk > 0:
                members.update(user_status=1)
                ret['ret'] = 0
                ret['msg'] = 'create user success'
            else:
                ret['ret'] = -1
                ret['msg'] = 'exception'
        else:
            ret['ret'] = -1
            ret['msg'] = 'unhandler exception'
    return HttpResponse(json.dumps(ret), mimetype='application/json')
