from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


dummy_data = [
    {
        'title': 'Would you be a good dolphin?',
        'author': 'Leroy',
        'score': '60%',
        'leaderboard': '10/2190'
    },
    {
        'title': 'Would you be a good doggo?',
        'author': 'Goodboi56',
        'score': '76%',
        'leaderboard': '643/23445'
    },
    {
        'title': 'States of the US',
        'author': 'D. J. Trump',
        'score': '100%',
        'leaderboard': '110/48432'
    }
]

# Create your views here.
def index(request):
    context = {}
    return render(request, 'rudumbapp/index.html', context)

def dashboard(request):
    context = {
        'historic': dummy_data
    }
    return render(request, 'rudumbapp/dashboard.html', context)