from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    # list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'firebase_id')
    fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'firebase_id')
    # pass


admin.site.register(CustomUser)
