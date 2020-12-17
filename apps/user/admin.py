from django.contrib import admin
from .models import CustomUser, UserAdmin

admin.site.register(CustomUser, UserAdmin)

