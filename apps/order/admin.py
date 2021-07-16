from django.contrib import admin
from .models import Order, OrderEvent, Invoice


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_email', 'token', 'user_id', 'is_active', 'voucher_id', 'firebase_id'
    )
#     list_display_links = ('id', 'username', 'email')
#     list_filter = ('is_staff', 'is_superuser')
#     search_fields = ('id', 'username', 'email', 'firebase_id')

admin.site.register(Order)
admin.site.register(OrderEvent)
admin.site.register(Invoice)
