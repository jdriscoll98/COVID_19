from rest_framework import serializers

from django.conf import settings

from apps.subscribers.models import Subscriber


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['telephone', 'location']
