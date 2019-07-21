from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/republican_result.html', context=None) #context={'party': party}, import the model
