from datetime import datetime
# from graphene import Enum # This is for Graphql v3
from django.db import models
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

Gender = ((1,'male'), (2,'female'), (0, None), (3, 'Not provided'))

# class Gender(Enum):
#     """Use this in GraphQL v3"""
#     none = 0
#     male = 1
#     female = 2
#     not_provided = 3


class CustomUser(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), null=True)
    firebase_id = models.TextField(null=True, unique=True)

    nickname = models.TextField(null=True)
    name = models.TextField(null=True)
    # gender = Gender(required=True) # Use this in GraphQL v3
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
        return self.firebase_id

    def anonymize(self):
        self.email = None
        self.name = None
        self.gender = 3
        self.phone = None
        self.birthday = datetime(2020,1,1)
        self.address = None
        self.is_active = False

        self.save(update_fields=['email', 'name', 'gender', 'phone', 'birthday', 'address', 'is_active'])


class PaidRecords(models):
    member_id = models.ForeignKey('CustomUser', to=CustomUser.firebase_id,
                                  on_delete=models.SET_NULL)
    type = models.CharField()
    amount = models.IntegerField()
    date = models.DateTimeField()
