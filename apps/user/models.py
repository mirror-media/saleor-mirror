from datetime import datetime

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from graphene_django import DjangoObjectType
from django.utils.translation import ugettext_lazy as _

Gender = ((1,'male'), (2,'female'), (0, None), (3, 'Not provided'))


class CustomUser(AbstractUser):
    class Meta:
        unique_together = ['firebase_id', 'email']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), null=True, unique=True)
    firebase_id = models.TextField(null=True)

    nickname = models.TextField(null=True)
    name = models.TextField(null=True)
    gender = models.IntegerField(choices=Gender, default=0)
    phone = models.TextField(null=True)
    birthday = models.DateField(null=True)

    country = models.TextField(null=True)
    city = models.TextField(null=True)
    district = models.TextField(null=True)

    address = models.TextField(null=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/',
                                      null=True, blank=True)

    def __str__(self):
        return f"FirebaseID: {self.firebase_id} , name: {self.name}"

    def anonymize(self):
        self.email = None
        self.name = None
        self.gender = 3
        self.phone = None
        self.birthday = datetime(2020,1,1)
        self.address = None
        self.is_active = False

        self.save(update_fields=['email', 'name', 'gender', 'phone', 'birthday', 'address', 'is_active'])


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone')
