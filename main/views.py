from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import fakemodel
from .models import handles
from tweets import get_tweets
from tweets import handle_exists
import random
import pandas as pd
import numpy as np
# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/index.html', context=None)

def getParty(request):
    """
        Write code to get 200 tweets of the handle given and check if there are 200 tweets
        Also handle errors to check if the twitter handle exists or not
        If the handle does not exist, then make it return -1 and in Django, show the user an error message saying that
        this user does not exist.


    """
    data = {'msg':'',
    'party': 'None'}
    if request.method == 'GET':
        hndle = request.GET.get('handle')
        if handle_exists.handle_exists(hndle):
            test = handles.objects.get(handle = hndle)
            data['party'] = test.party
            data['msg'] = 'She exists'
        else:
            data['msg'] = "Hello"
    """
        Fake model of the form

        percentage = predict(tweets)  # This will give the percentage on how likely the handle is a democrat.

        For now this is a dummy function
    """

    percentage = random.uniform(0, 1)
    return JsonResponse(data)
