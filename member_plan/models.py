from django.db import models
from apps.user.models import CustomUser


class MemberPlan(models):
    member_id = models.ForeignKey(to=CustomUser.firebase_id)
    plan_type = models.CharField()
    start_date = models.DateField()
    due_date = models.DateField()

