from django.contrib import admin
from service.models import ServiceType, Service, SerMerchant, SerRoom, Beautician, CardPool

admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(SerMerchant)
admin.site.register(SerRoom)
admin.site.register(Beautician)
admin.site.register(CardPool)
