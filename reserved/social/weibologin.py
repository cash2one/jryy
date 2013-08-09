#-*- coding:utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import UNUSABLE_PASSWORD
from social.models import UserExtend
from django.contrib.auth import authenticate, login

from utils.weibo import APIClient

APP_KEY = '2647007612'
APP_SECRET = '1e3740617ac93088b1bb80a246c8c38a'
CALLBACK_URL = 'http://dev.zh.ongl.in/login/weibo_callback.html'
CALLBACK_URL = 'http://127.0.0.1:8000/login/weibo_callback.html'


def jump_weibo_login(request):
    client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    url = client.get_authorize_url(redirect_uri = CALLBACK_URL)
    return HttpResponseRedirect(url)


def sina_id_to_user(uid):

    DEFAULT_EMAIL = ''
    username = 'SINA_%s'%uid
    if not UserExtend.objects.filter( sina_id = uid).exists():
        user = UserExtend.objects.create_user(username,
                    DEFAULT_EMAIL, UNUSABLE_PASSWORD)

        user.sina_id = uid
        user.save()
        return user

    return UserExtend.objects.get(sina_id=uid)

def weibo_callback(request):
    client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    code = request.GET['code']
    r = client.request_access_token(code)
    user = sina_id_to_user(r.uid)

    user = authenticate(remote_user=user)

    login(request, user)

    request.session['oauth_token'] = r
    return HttpResponseRedirect('/')

