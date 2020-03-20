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
from Crypto.Random import random
from twilio.rest import Client
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import BasePermission

from pprint import pprint

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all().order_by('-date_joined')
    serializer_class = SubscriberSerializer

    def list(self, request):
        return Response({})

    def retrieve(self, request, pk=None):
        return Response({})
    

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
            return Response(data={'error':'Invalid Code'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False, url_path='set_options', url_name='set_options')
    def set_options(self, request):
        data = request.POST
        subscriber = Subscriber.objects.get(telephone=data.get('number'))
        if not subscriber.option:
            subscriber.option = True
            subscriber.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='reset', url_name='reset')
    def reset(self, request):
        data = request.POST
        subscriber = Subscriber.objects.get(telephone=data.get('number'))
        if subscriber.option:
            subscriber.option = False
            subscriber.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='begin_flow', url_name='begin_flow')
    def begin_flow(self, request):
        data = request.data
        subscriber = Subscriber.objects.get(telephone=data['number'])
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        execution = client.studio.v1.flows('FW048094fe4cacdbaa71d02e7f5af1ebb1').executions.create(
            to=data['number'], from_='+13523204710', parameters={'number':data['number']})
        if execution:
            data = {
                'url': execution.url
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['post'], detail=False, url_path='unsubscribe', url_name='unsubscribe')
    def unsubscribe(self, request):
        data = request.data
        try:
            subscriber = Subscriber.objects.get(telephone=data['number'])
            subscriber.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    @action(methods=['post'], detail=False, url_path='resend', url_name='resend')
    def resend(self, request):
        data = request.data
        try:
            subcriber = Subscriber.objects.get(telephone=data['telephone'])
            key = random.randint(100000, 999999)
            subcriber.key = key
            subcriber.save()
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
            body=f'Your validation code is {key}',
            from_="13523204710",
            to=data['telephone']
            )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

