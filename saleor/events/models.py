from django.db import models


# Create your models here.

class Events(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length=255)
    description = models.TextField()
