import requests

from django.conf import settings
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.subscribers.models import Subscriber
from apps.subscribers.serializers import SubscriberSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-date_joined')
    serializer_class = SubscriberSerializer

