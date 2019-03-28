from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from .forms import UserRegistrationForm
from django.http import Http404

from django.core.paginator import Paginator
from next_prev import next_in_order

from .forms import (
    BookFormset,
    BookModelFormset,
    BookModelForm,
    AuthorFormset
)

from .models import Quiz, Category, Question

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

def quiz_form(request):
    template_name = 'quiz/quiz_form.html'
    if request.method == 'GET':
        bookform = BookModelForm(request.GET or None)
        formset = AuthorFormset(queryset=Quiz.objects.none())
    elif request.method == 'POST':
        bookform = BookModelForm(request.POST)
        formset = AuthorFormset(request.POST)
        if bookform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            book = bookform.save()
            for form in formset:
                # so that `book` instance can be attached.
                author = form.save(commit=False)
                author.question = book
                author.choice1 = "ddd"
                author.save()
            return redirect('store:book_list')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,
    })

def quiz(request, id):
    template_name = 'quiz/quiz.html'

    quiz = get_object_or_404(Quiz, pk=id)

    return render(request, template_name, {
        'quiz' : quiz,
    })


def results_quiz(request, id):
    template_name = 'quiz/result.html'

    if request.method == 'POST':


        #A VOIR
        i = 0
        j = 1
        result = []
        quiz = get_object_or_404(Quiz, pk=id)
        for q in quiz.question_set.all():
            input_keys = request.POST.get("optionsRadios" + str(j))
            if input_keys[i] == q.answer:
                result.append(True)
            else:
                result.append(False)
            i = i+1
            j = j + 1

        return render(request, template_name, {
            'result': input_keys
        })


