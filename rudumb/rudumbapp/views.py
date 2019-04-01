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
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.forms import model_to_dict
from .models import Quiz, Category

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
        question_formset=Question_FormSet(request.POST, request.FILES)
        quiz_form = QuizCreationForm(request.POST, request.FILES)
        print(quiz_form.errors)
        #Checking the if the form is valid
        if question_formset.is_valid() and quiz_form.is_valid():
            
            #To save we have loop through the formset
            #quiz_form.save(commit = False)
            #quiz_form.image = request.FILES['image']
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