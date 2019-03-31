from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.http import Http404
from datetime import datetime

from .models import Quiz, Category, Stat

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
        category = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return render(request, 'index/home.html', {'category': category})


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


def quiz(request, id):
    template_name = 'quiz/quiz.html'

    quiz = get_object_or_404(Quiz, pk=id)

    return render(request, template_name, {
        'quiz': quiz,
    })


def results_quiz(request, id):
    template_name = 'quiz/result.html'

    if request.method == 'POST':
        i = 1
        trueAnswer = 0;
        result = []
        input_keys = []
        quiz = get_object_or_404(Quiz, pk=id)
        for key, value in request.POST.items():
            input_keys.append(value)
        for q in quiz.question_set.all():
            if int(input_keys[i]) == q.answer:
                result.append(True)
                trueAnswer = trueAnswer + 1;
            else:
                result.append(False)
            i = i + 1

        lenght = len(result)

        if request.session.get('_auth_user_id') is not None:
            user = request.session.get('_auth_user_id')

            if not Stat.objects.filter(quiz_id=id, user_id=user).exists() :
                Stat.objects.create(result_quiz=trueAnswer, date_quiz_done=datetime.now(), quiz_id=id, user_id=user)
            else:
                Stat.objects.update(result_quiz=trueAnswer, date_quiz_done=datetime.now())


        return render(request, template_name, {
            'result': result,
            'trueAnswer': trueAnswer,
            'lenght': lenght,
            'quiz': quiz
        })
