#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test, login_required

from models import Service, ServiceType, Beautician, SerMerchant, SerRoom
from orders.models import Order

from forms import LoginForm
from forms import ServiceForm
from forms import OrderForm

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def detail(request):
    return render_to_response('manage/base.html', {}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def calendar(request):
    return render_to_response('manage/calendar.html', {}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def service(request):
    '''
    服务项目管理
    '''
    userid = request.user.id
    services = Service.objects.all()

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            print request.user
            service = form.save(commit=False)
            merch = SerMerchant.objects.get(mer_founder=request.user)
            service.merchant = merch
            service.save()
            return HttpResponseRedirect('/service')
        else:
            print 'error'
    else:
        form = ServiceForm() #获得表单对象
    return render_to_response('manage/service.html', {'form':form,'services':services}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def category(request):
    '''
    分类管理
    '''
    sertypes = ServiceType.objects.all()
    return render_to_response('manage/category.html', {'sertypes':sertypes}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def rooms(request):
    '''
    房间管理
    '''
    rooms = SerRoom.objects.all()
    return render_to_response('manage/rooms.html', {'rooms':rooms}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def beautician(request):
    '''
    技师管理
    '''
    btcs = Beautician.objects.all()
    return render_to_response('manage/beautician.html', {'btcs':btcs},context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_authenticated(), login_url='/signin')
def orders(request):
    '''
    订单管理
    '''
    userid = request.user.id
    merch = SerMerchant.objects.get(id=3)
    orders = Order.objects.filter(merchant=merch)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print request.user
            order = form.save(commit=False)
            merch = SerMerchant.objects.get(mer_founder=request.user)
            order.merchant = merch
            order.save()
            return HttpResponseRedirect('/orders')
        else:
            print 'error'
    else:
        form = OrderForm() #获得表单对象
    return render_to_response('manage/orders.html', {'form':form,'orders':orders}, context_instance=RequestContext(request))




def signin(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            from django.contrib.auth import authenticate, login
            #import pdb
            #pdb.set_trace()
            user = authenticate(username=loginform.cleaned_data['username'], password=loginform.cleaned_data['password'])
            print 'auth',user
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('manage/login.html',
                                      {'loginform': loginform, 'username':request.POST['username']},
                                      context_instance=RequestContext(request))


    return render_to_response('manage/login.html',
                                {},
                                context_instance=RequestContext(request))

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/signin')
