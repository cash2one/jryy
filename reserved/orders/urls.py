
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^calendar$', 'orders.views.calendar', name='cal'),
    url(r'^day/(?P<datestr>\d+)', 'orders.views.day_detail', name='day'),
    url(r'^choose_service/(?P<datestr>\d+)/(?P<timestr>\d+)', 'orders.views.choose_service', name='choose_service'),
    url(r'^order/(?P<datestr>\d+)/(?P<timestr>\d+)', 'orders.views.order', name='order'),
    #social login
    url(r'^s_login$', 'orders.views.social_login', name='social_login'),
)
