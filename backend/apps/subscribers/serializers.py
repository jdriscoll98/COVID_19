import re

from django.conf import settings
from rest_framework import serializers

from apps.subscribers.models import Subscriber
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client
from Crypto.Random import random


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['telephone', 'location', 'key']

    def validate_telephone(self, value):
        if not re.match("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", value):
            raise serializers.ValidationError("Please enter a valid phone number")
        return value

    def create(self, validated_data):
        client = Client(TWILIO_ACCOUNT_SID,
                        TWILIO_AUTH_TOKEN)
        key = random.randint(100000, 999999)
        message = client.messages.create(
            body=f'Your validation key is {key}',
            from_="13523204710",
            to=validated_data.get("telephone")
        )
        return Subscriber.objects.create(key=key, **validated_data)
        
