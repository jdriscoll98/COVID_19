from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import logout

from django.conf.urls import include

from config.api import api



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include(api.urls)), 
]

