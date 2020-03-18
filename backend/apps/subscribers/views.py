import requests
import json

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.subscribers.models import Subscriber
from apps.subscribers.serializers import SubscriberSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-date_joined')
    serializer_class = SubscriberSerializer

    @action(methods=['post'], detail=False, url_path='verify', url_name='verify')
    def verify(self, request):
        data = request.data
        print(data)
        number = data['telephone']
        key = data['key']
        subscriber = Subscriber.objects.get(telephone=number)
        if key == subscriber.key:
            subscriber.verified = True
            subscriber.save()
            print('verified')
            return Response(status=status.HTTP_200_OK)
        else:
            print('not verified')
            return Response(status=status.HTTP_401_UNAUTHORIZED)


