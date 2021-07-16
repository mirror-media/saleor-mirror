from django.db import models
from apps.user.models import CustomUser

class PurchasedArticle(models):
    member_id = models.ForeignKey(to=CustomUser.firebase_id)

