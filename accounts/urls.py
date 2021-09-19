from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LoginView

from rest_framework.authtoken import views

urlpatterns = [
    path('login',LoginView.as_view(),name='login'),
    path('',include('django.contrib.auth.urls')),
    path('api-auth-token/',views.obtain_auth_token,name='api-auth-token'),
]