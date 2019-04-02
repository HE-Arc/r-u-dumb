from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    url('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/<int:id>/results/', views.results_quiz, name='results'),
    path('quiz/<int:id>/', views.quiz, name='quiz'),
    path('quizCreationForm/', views.quizCreationForm, name='quizCreationForm'),
    path('search_quiz/', views.search_quiz, name='search_quiz'),
    path('category/', views.category_form, name='category'),
]
