from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView # new

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
]