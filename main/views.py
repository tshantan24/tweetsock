from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Handle
# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/header.html', context=None) #context={'party': party}, import the model

def handle_exists(request):
	if request.method == 'GET':
		handle = request.GET.get('handle')
		list_of_handles_raw = list(Handle.objects.values('handle','party'))
		list_of_handles = []
		for i in range(len(list_of_handles_raw)):
			list_of_handles.append(list_of_handles_raw[i]['handle'])
		if handle in list_of_handles:
			test = Handle.objects.get(handle = handle)
			party = test.party
		else:
			return "handle doesnt exist"

	return render(request=request, template_name='main/main.html', context={'party': party})