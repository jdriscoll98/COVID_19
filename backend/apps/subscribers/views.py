import requests
import json
from django.views.generic import View
from django.utils.decorators import method_decorator
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse


from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from apps.subscribers.models import Subscriber
from apps.subscribers.serializers import SubscriberSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-date_joined')
    serializer_class = SubscriberSerializer

    @action(methods=['post'], detail=False, url_path='verify', url_name='verify')
    def verify(self, request):
        data = request.data
        number = data['telephone']
        key = data['key']
        subscriber = Subscriber.objects.get(telephone=number)
        if key == subscriber.key:
            subscriber.verified = True
            subscriber.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False, url_path='set_options', url_name='set_options')
    def set_options(self, request):
        data = request.POST
        subscriber = Subscriber.objects.get(telephone=data.get('number'))
        subscriber.options = data.get('options')
        subscriber.save()
        return Response(status=status.HTTP_200_OK)


