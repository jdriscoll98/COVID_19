from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    telephone = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    option = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    key = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.telephone} | {self.verified}"
