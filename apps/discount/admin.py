from django.contrib import admin
from .models import Voucher, VoucherCustomer, Sale


# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'user_email', 'token', 'user_id', 'is_active', 'voucher_id', 'firebase_id'
#     )
#     list_display_links = ('id', 'username', 'email')
#     list_filter = ('is_staff', 'is_superuser')
#     search_fields = ('id', 'username', 'email', 'firebase_id')

admin.site.register(VoucherCustomer)
admin.site.register(Voucher)
admin.site.register(Sale)
