from django.db import models
from apps.user.models import CustomUser

class PaidRecords(models):
    member_id = models.ForeignKey(to=CustomUser.firebase_id)
    item_type = models.CharField()
    paid_time = models.DateField()
