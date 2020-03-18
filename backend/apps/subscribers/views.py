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

from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client


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
        print(data)
        subscriber = Subscriber.objects.get(telephone=data.get('number')[0])
        subscriber.options = data.get('option')[0]
        subscriber.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='begin_flow', url_name='begin_flow')
    def begin_flow(self, request):
        data = request.data
        print(data)
        subscriber = Subscriber.objects.get(telephone=data['telephone'])
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        execution = client.studio.v1.flows('FW048094fe4cacdbaa71d02e7f5af1ebb1').executions.create(
            to=data['telephone'], from_='+13523204710')
        if execution:
            data = {
                'url': execution.url
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

