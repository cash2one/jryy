from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'social.weibologin',
    url(r'^jump_weibo_login.html$', 'jump_weibo_login', name ="jump_weibo_login"),    url(r'^weibo_callback.html$', 'weibo_callback'),
)
