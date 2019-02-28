from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    context = {}
    return render(request, 'rudumbapp/index.html', context)