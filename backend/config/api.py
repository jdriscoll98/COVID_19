from rest_framework import routers
from apps.subscribers.views import SubscriberViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'subscribers', SubscriberViewSet)