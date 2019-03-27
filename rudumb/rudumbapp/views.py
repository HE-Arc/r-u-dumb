from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import Quiz, Category

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
def home(request):
    try:
        quiz_list = Quiz.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(quiz_list, 10)
        quizz = paginator.page(page)


    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")
    return render(request, 'index/home.html', {'quizz': quizz})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    context = {
        'historic': dummy_data
    }
    return render(request, 'dashboard.html', context)


def quizCreationForm(request):
    categories = Category.objects.all()

    return render(request, 'quizCreationForm.html', categories)

