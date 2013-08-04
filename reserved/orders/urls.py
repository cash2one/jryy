
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^calendar$', 'orders.views.calendar', name='cal'),
    url(r'^day/(?P<datestr>\d+)', 'orders.views.day_detail', name='day'),
)
