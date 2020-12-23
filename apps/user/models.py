from datetime import datetime

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from graphene_django import DjangoObjectType
from django.utils.translation import ugettext_lazy as _

Gender = ((1,'male'), (2,'female'), (0,'Null'), (3, 'Not provided'))


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    firebase_id = models.CharField(max_length=50, null=True, unique=True)
    nickname = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=20, null=True)
    gender = models.IntegerField(choices=Gender, default=0)
    phone = models.CharField(max_length=20, null=True)
    birthday = models.DateField(default=datetime(2020,1,1))

    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)

    address = models.CharField(max_length=200, null=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/',
                                      null=True, blank=True)

    # objects = CustomUserManager()

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
