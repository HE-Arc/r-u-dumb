from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, QuizCreationForm, QuizQuestionForm
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.forms import formset_factory

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
    
    #We are creating a formset out of the ContactForm
    Question_FormSet = formset_factory(QuizQuestionForm)
    #The Template name where we are going to display it
    template_name="quizCreationForm.html"

    #Overiding the get method
    if request.method == 'GET':
        #Creating an Instance of formset and putting it in context dict
        context={
                'question_form': Question_FormSet(),
                'quiz_form': QuizCreationForm()
                }

        return render(request, template_name, context)

    if request.method == 'POST':
        question_formset=Question_FormSet(request.POST)
        quiz_form = QuizCreationForm(request.POST)
        print(quiz_form.errors)
        print(question_formset.errors)
        #Checking the if the form is valid
        if question_formset.is_valid() and quiz_form.is_valid():
            
            #To save we have loop through the formset
            q = quiz_form.save()
            for question in question_formset:
                #Saving in the contacts models
                questionObject = question.save(commit=False)
                questionObject.quiz = q

                questionObject.save()

            return HttpResponseRedirect('/')

        else:
            context={
                    'question_form': Question_FormSet(),
                    'quiz_form': QuizCreationForm()

                    }

            return render(request, template_name,context)