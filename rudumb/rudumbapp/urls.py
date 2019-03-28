from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/', views.register),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('quizCreationForm', views.quizCreationForm, name='quizCreationForm'),
]

