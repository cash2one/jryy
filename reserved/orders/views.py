# Create your views here.
import datetime
import random
from service.models import Service, ServiceType, Beautician, SerMerchant, SerRoom
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext

def calendar(request):
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


