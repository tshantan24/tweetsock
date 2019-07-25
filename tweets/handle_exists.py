from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from tweets import get_tweets
from main.models import handles


def handle_exists(handle):
    list_of_handles_raw = list(handles.objects.values('handle'))
    list_of_handles = []
    x = False
    for i in range(len(list_of_handles_raw)):
        list_of_handles.append(list_of_handles_raw[i]['handle'])
    if handle in list_of_handles:
        x = True
    return x
