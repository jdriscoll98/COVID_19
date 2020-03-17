from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    telephone = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)