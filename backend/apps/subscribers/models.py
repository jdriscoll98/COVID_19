from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    telephone = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=500)
    option = models.CharField(max_length=4, blank=True, default="none")
    verified = models.BooleanField(default=False)
    key = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.telephone} | {self.verified}"
