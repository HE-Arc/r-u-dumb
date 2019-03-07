from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView # new

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', TemplateView.as_view(template_name='rudumbapp/index.html'), name='index'),
    path('quiz/', TemplateView.as_view(template_name='rudumbapp/index.html'), name='quiz')

]