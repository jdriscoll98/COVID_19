import re
import json

from django.conf import settings
from rest_framework import serializers

from apps.subscribers.models import Subscriber
from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.rest import Client

from Crypto.Random import random
import phonenumbers



class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['telephone', 'location', 'key']

    def validate_telephone(self, value):
        if not re.match("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", value):
            raise serializers.ValidationError("Please enter a valid phone number")
        parsed_number = phonenumbers.parse(value, "US")
        number = f"+{parsed_number.country_code}{parsed_number.national_number}"
        if Subscriber.objects.filter(telephone=number).exists():
            subscriber = Subscriber.objects.get(telephone=number)
            if subscriber.verified:
                raise serializers.ValidationError("Sorry, this number is already registered")
            else:
                subscriber.delete()
        return value

    def validate_location(self, value):
        if value == "{}":
            raise serializers.ValidationError(
                "Please user the autocomplete feature for the location")
        return value

    def create(self, validated_data):
        telephone = validated_data.pop("telephone")
        client = Client(TWILIO_ACCOUNT_SID,
                        TWILIO_AUTH_TOKEN)
        key = random.randint(100000, 999999)
        message = client.messages.create(
            body=f'Your validation key is {key}',
            from_="13523204710",
            to=telephone
        )
        return Subscriber.objects.create(key=key, telephone=message.to, **validated_data)
    
