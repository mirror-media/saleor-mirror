from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'firebase_id'
    )
    list_display_links = ('id', 'username', 'email')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('id', 'username', 'email', 'firebase_id')


admin.site.register(CustomUser, UserAdmin)
