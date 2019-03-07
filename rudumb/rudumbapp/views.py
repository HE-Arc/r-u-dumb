from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Quizzes 



# Create your views here.
def index(request):
    context = {

        'quizz_list' : "test"
    }
    return render(request, 'rudumbapp/index.html', context)