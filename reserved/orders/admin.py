from django.contrib import admin
from orders.models import Customer, Order, OrderDetail, CustomerPreference, OrderComment, BeauticianComment   

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(CustomerPreference)
admin.site.register(OrderComment)
admin.site.register(BeauticianComment)
