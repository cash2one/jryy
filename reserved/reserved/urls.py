from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reserved.views.home', name='home'),
    # url(r'^reserved/', include('reserved.foo.urls')),

    url(r'^$', 'service.views.detail', name='home'),
    url(r'^beautician$', 'service.views.beautician', name='beautician'),
    url(r'^rooms$', 'service.views.rooms', name='rooms'),
    url(r'^category$', 'service.views.category', name='category'),
    url(r'^calendar$', 'service.views.calendar', name='calendar'),
    url(r'^service$', 'service.views.service', name='service'),
    url(r'^orders$', 'service.views.orders', name='orders'),
    url(r'^members$', 'service.views.members', name='members'),


    url(r'^signin$', 'service.views.signin', name='signin'),
    url(r'^logout$', 'service.views.logout', name='logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^client/', include('orders.urls')),
    url(r'^login/', include('social.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
