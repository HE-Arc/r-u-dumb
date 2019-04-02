from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, QuizCreationForm, QuizQuestionForm, CategoryForm
from django.http import Http404
from .static.fusioncharts import FusionCharts

from collections import OrderedDict

from .models import Quiz, Category, Stat, AuthUser

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.forms import formset_factory
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.forms import model_to_dict

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
@csrf_protect
def home(request):
    
    
    quiz_list = Quiz.objects.all().order_by("-date")
    page = request.GET.get('page', 1)

    paginator = Paginator(quiz_list, 10)
    quizz = paginator.page(page)
    return render(request, 'index/home.html', {'quizz': quizz}, RequestContext(request))

def search_quiz(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        json_datas = {}
        quizz_search = Quiz.objects.filter(name__icontains=search_text)

        for quiz in quizz_search:
            json_datas[quiz.id] = [quiz.name, quiz.image.url]

        return JsonResponse(
            json_datas
        )
    

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


def category_form(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data
            name = category['name']
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name)
                return HttpResponseRedirect('/category')
            else:
                raise forms.ValidationError('Looks like a category with the same name exists')

    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form})


def dashboard(request):
    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "How do you stack up?"
    chartConfig["xAxisName"] = "Score"
    chartConfig["yAxisName"] = "Number of players at that score"
    chartConfig["theme"] = "fusion"
    dataSource["chart"] = chartConfig
    dataSource["data"] = []

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


    current_user = request.user.id
    n_quiz = Stat.objects.all().count()
    n_done = passed_quiz = Stat.objects.filter(user=current_user).count()

    #Calcul de la moyenne de l'utilisateur courant
    passed_quiz = Stat.objects.filter(user=current_user)

    #Compteur
    player_total_score = 0
    for quiz in passed_quiz.iterator():
        player_total_score += quiz.result_quiz

    #Division par zéro
    if n_quiz == 0:
        ratio = "x/0"
    else:
        ratio = n_done/n_quiz*100


    #Calcul de la moyenne globale des autres utilisateurs
    passed_quiz_by_others = Stat.objects.exclude(user=current_user)

    #Compteurs
    others_total_score = 0
    others_n = 0
    for quiz in passed_quiz_by_others.iterator():
        others_total_score += quiz.result_quiz
        others_n += 1

    #Division par zéro
    if others_n == 0:
        others_average = "x/0"
    else:
        others_average = others_total_score/others_n

    # Populate the gaussian
    users = AuthUser.objects.all()

    # Creer dict
    gaussian = dict()
    total_score = 0
    # Pour chaque utilisateur
    for user in users.iterator():
        user_points = 0
        quiz_user = Stat.objects.filter(user=user)
        # Compte ses points totauxs
        for quiz in quiz_user.iterator():
            user_points += quiz.result_quiz
        # Enter data in gaussian dict
        if user_points in gaussian:
            gaussian[user_points] += 1
        else:
            gaussian[user_points] = 1
        
        # Remember the user score
        if user == current_user:
            total_score = user_points

    #Sort the gaussian and fill it with the zeros
    right_limit = max(gaussian.keys())
    for i in range(0, right_limit):
        # Fill in the blanks
        if i not in gaussian:
            gaussian[i] = 0

    
    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts. 
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.
    # Iterate through the data in `incomplete_gaussian` and insert in to the `dataSource['data']` list.
    for key, value in gaussian.items():
        data = {}
        data["label"] = key
        data["value"] = value
        if key == total_score:
            data["color"] = "#FF4500" #Custom Color
        dataSource["data"].append(data)

    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1", "100%", "30%", "distribution_chart", "json", dataSource)

    scores = {
        'total_completed': n_done,
        'completed_ratio': ratio,
        'other_players_avg': others_average,
        'total_score': total_score
    }

    context = {
        'historic': passed_quiz,
        'score': scores,
        'distribution': column2D.render()
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

            if not Stat.objects.filter(quiz_id=id, user_id=user).exists():
                Stat.objects.create(result_quiz=trueAnswer, date_quiz_done=datetime.now(), quiz_id=id, user_id=user)
            else:
                Stat.objects.update(result_quiz=trueAnswer, date_quiz_done=datetime.now())

        return render(request, template_name, {
            'result': result,
            'trueAnswer': trueAnswer,
            'lenght': lenght,
            'quiz': quiz
        })
    else:
        return render(request, template_name)


def quizCreationForm(request):
    # We are creating a formset out of the ContactForm
    Question_FormSet = formset_factory(QuizQuestionForm)
    # The Template name where we are going to display it
    template_name = "quizCreationForm.html"

    # Overiding the get method
    if request.method == 'GET':
        # Creating an Instance of formset and putting it in context dict
        context = {
            'question_form': Question_FormSet(),
            'quiz_form': QuizCreationForm()
        }

        return render(request, template_name, context)

    if request.method == 'POST':
        question_formset = Question_FormSet(request.POST, request.FILES)
        quiz_form = QuizCreationForm(request.POST, request.FILES)
        print(quiz_form.errors)
        # Checking the if the form is valid
        if question_formset.is_valid() and quiz_form.is_valid():

            # To save we have loop through the formset
            # quiz_form.save(commit = False)
            # quiz_form.image = request.FILES['image']
            q = quiz_form.save()
            for question in question_formset:
                # Saving in the contacts models
                questionObject = question.save(commit=False)
                questionObject.quiz = q
                questionObject.save()
            return HttpResponseRedirect('/quiz/'+str(q.id))

        else:
            context = {
                'question_form': Question_FormSet(),
                'quiz_form': QuizCreationForm()
            }
            return render(request, template_name, context)


