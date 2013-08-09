from django.contrib import admin
from orders.models import Customer, Order, OrderDetail, CustomerPreference, OrderComment, BeauticianComment

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_begin', 'order_room', 'order_beautician', 'order_state', 'create_time')
    search_fields = ('user',)
    list_filter = ('merchant', 'order_beautician', 'order_state')

admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(CustomerPreference)
admin.site.register(OrderComment)
admin.site.register(BeauticianComment)
