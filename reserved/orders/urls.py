from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^calendar$', 'orders.views.calendar', name='cal'),
)
