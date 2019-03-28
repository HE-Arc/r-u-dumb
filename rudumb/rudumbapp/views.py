from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.http import Http404
from .static.fusioncharts import FusionCharts

from collections import OrderedDict

from .models import Quiz, Category


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
    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "How do you stack up?"
    chartConfig["xAxisName"] = "Score"
    chartConfig["yAxisName"] = "Number of players at that score"
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["0"] = 30
    chartData["1"] = 45
    chartData["2"] = 54
    chartData["3"] = 70
    chartData["4"] = 140
    chartData["5"] = 167
    chartData["6"] = 234
    chartData["7"] = 256
    chartData["8"] = 189
    chartData["9"] = 165
    chartData["10"] = 89


    dataSource["chart"] = chartConfig
    dataSource["data"] = []
    
    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts. 
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1", "100%", "30%", "distribution_chart", "json", dataSource)

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

    scores = {
        'total_completed': '37',
        'global_ratio': '78%',
        'completed_ratio': '60%',
        'global_leaderboard': '10/2190'
    }

    context = {
        'historic': dummy_data,
        'score': scores,
        'distribution': column2D.render()
    }
    return render(request, 'dashboard.html', context)

