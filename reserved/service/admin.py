from django.contrib import admin
from service.models import ServiceType, Service, SerMerchant

admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(SerMerchant)
