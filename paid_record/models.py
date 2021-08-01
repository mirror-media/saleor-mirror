from django.db import models
from apps.user.models import CustomUser

class PaidRecords(models):
    member_id = models.ForeignKey(CustomUser, to=CustomUser.firebase_id)
    merchant_order_no = models.CharField()
    item_type = models.CharField()
    paid_time = models.DateField()

class Transaction(models):
    member_id = models.ForeignKey(CustomUser)
    merchant_order_no = models.CharField()

class Invoice(models):
    member_id = models.ForeignKey(CustomUser)
    merchant_order_no = models.ForeignKey(Transaction)
    invoice_number = models.CharField()
    invoice_date = models.DateTimeField()
    amount = models.IntegerField()


