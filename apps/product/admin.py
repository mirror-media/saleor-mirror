from django.contrib import admin
from .models import Product


# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'user_email', 'token', 'user_id', 'is_active', 'voucher_id', 'firebase_id'
#     )

admin.site.register(Product)
